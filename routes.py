import json

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .models import User
from .schemas import FeedbackRequest, UserInput, WorkoutPlan
from .templates import templates
from .updated_plan import update_workout_plan

router = APIRouter()
settings = get_settings()


def _plan_to_json(plan: WorkoutPlan) -> str:
    return json.dumps(plan.model_dump(), ensure_ascii=False, indent=2)


def _load_user(db: Session, user_id: str) -> User | None:
    return db.scalar(select(User).where(User.user_id == user_id))


def _upsert_user(
    db: Session,
    user_input: UserInput,
    workout: WorkoutPlan,
    nutrition_tip: str,
) -> User:
    user = _load_user(db, user_input.user_id)

    if user is None:
        user = User(
            user_id=user_input.user_id,
            username=user_input.username,
            age=user_input.age,
            weight=user_input.weight,
            goal=user_input.goal,
            intensity=user_input.intensity,
            original_plan=_plan_to_json(workout),
            nutrition_tip=nutrition_tip,
        )
        db.add(user)
    else:
        user.username = user_input.username
        user.age = user_input.age
        user.weight = user_input.weight
        user.goal = user_input.goal
        user.intensity = user_input.intensity
        user.original_plan = _plan_to_json(workout)
        user.updated_plan = None
        user.nutrition_tip = nutrition_tip

    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "FitBuddy – AI Fitness Plan Generator"},
    )


@router.get("/api/health")
def health():
    return {"status": "ok", "service": "FitBuddy"}


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout_html(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user_input = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
        workout = generate_workout_gemini(user_input)
        tip = generate_nutrition_tip_with_flash(user_input.goal)

        user = _upsert_user(
            db,
            user_input,
            workout,
            f"{tip.tip} {tip.recovery_note}",
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "title": "Your FitBuddy Plan",
                "user": user,
                "workout": workout,
                "nutrition_tip": tip,
                "updated": False,
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            status_code=500,
            context={"title": "FitBuddy Error", "message": str(exc)},
        )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback_html(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        feedback_model = FeedbackRequest(
            user_id=user_id,
            feedback=feedback,
        )
        user = _load_user(db, feedback_model.user_id)

        if user is None:
            return templates.TemplateResponse(
                request=request,
                name="error.html",
                status_code=404,
                context={
                    "title": "User Not Found",
                    "message": "No FitBuddy user was found for that User ID.",
                },
            )

        original = WorkoutPlan.model_validate_json(user.original_plan)
        revised = update_workout_plan(
            original_plan=original,
            feedback=feedback_model.feedback,
            goal=user.goal,
            intensity=user.intensity,
        )

        user.updated_plan = _plan_to_json(revised)
        db.commit()
        db.refresh(user)

        tip = generate_nutrition_tip_with_flash(user.goal)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "title": "Updated FitBuddy Plan",
                "user": user,
                "workout": revised,
                "nutrition_tip": tip,
                "updated": True,
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            status_code=500,
            context={"title": "FitBuddy Error", "message": str(exc)},
        )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    admin_key: str = Query(default=""),
    db: Session = Depends(get_db),
):
    if admin_key != settings.admin_key:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            status_code=403,
            context={
                "title": "Admin Access Required",
                "message": "Use the configured ADMIN_KEY to open the dashboard.",
            },
        )

    users = db.scalars(
        select(User).order_by(User.created_at.desc())
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"title": "FitBuddy Admin Dashboard", "users": users},
    )


@router.post("/api/generate-workout")
def generate_workout_api(
    user_input: UserInput,
    db: Session = Depends(get_db),
):
    workout = generate_workout_gemini(user_input)
    tip = generate_nutrition_tip_with_flash(user_input.goal)

    user = _upsert_user(
        db,
        user_input,
        workout,
        f"{tip.tip} {tip.recovery_note}",
    )

    return {
        "user": user_input.model_dump(),
        "workout_plan": workout.model_dump(),
        "nutrition_tip": tip.model_dump(),
        "database_id": user.id,
    }


@router.post("/api/submit-feedback")
def submit_feedback_api(
    feedback: FeedbackRequest,
    db: Session = Depends(get_db),
):
    user = _load_user(db, feedback.user_id)

    if user is None:
        return JSONResponse(
            status_code=404,
            content={"detail": "User not found."},
        )

    original = WorkoutPlan.model_validate_json(user.original_plan)
    revised = update_workout_plan(
        original_plan=original,
        feedback=feedback.feedback,
        goal=user.goal,
        intensity=user.intensity,
    )

    user.updated_plan = _plan_to_json(revised)
    db.commit()

    return {
        "user_id": user.user_id,
        "updated_plan": revised.model_dump(),
    }
