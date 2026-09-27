from unittest.mock import patch

from app.schemas import (
    Exercise,
    NutritionTip,
    WorkoutDay,
    WorkoutPlan,
)


def fake_plan():
    return WorkoutPlan(
        title="Demo 7-Day Wellness Plan",
        overview="A safe test plan.",
        days=[
            WorkoutDay(
                day=f"Day {i}",
                focus="General wellness",
                warm_up="5 minutes of easy movement.",
                exercises=[
                    Exercise(
                        name="Bodyweight squat",
                        sets="2",
                        reps_or_duration="8 reps",
                        rest="60 sec",
                    )
                ],
                cool_down="Easy stretching and recovery.",
            )
            for i in range(1, 8)
        ],
        safety_note="Use comfortable effort and recover as needed.",
    )


def fake_tip():
    return NutritionTip(
        tip="Choose balanced meals with a variety of ordinary foods.",
        recovery_note="Hydrate regularly and prioritize sleep.",
    )


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text
    assert "Generate 7-Day Plan" in response.text


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "FitBuddy"}


def test_invalid_user_input(client):
    payload = {
        "username": "A",
        "user_id": "x",
        "age": 10,
        "weight": 10,
        "goal": "invalid",
        "intensity": "invalid",
    }
    response = client.post("/api/generate-workout", json=payload)
    assert response.status_code == 422


def test_admin_requires_key(client):
    response = client.get("/view-all-users")
    assert response.status_code == 403


@patch("app.routes.generate_nutrition_tip_with_flash", side_effect=lambda goal: fake_tip())
@patch("app.routes.generate_workout_gemini", side_effect=lambda user: fake_plan())
def test_generate_api(mock_workout, mock_tip, client):
    payload = {
        "username": "Demo User",
        "user_id": "demo-001",
        "age": 20,
        "weight": 65,
        "goal": "general wellness",
        "intensity": "medium",
    }

    response = client.post("/api/generate-workout", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["database_id"] >= 1
    assert len(body["workout_plan"]["days"]) == 7
    assert body["nutrition_tip"]["tip"]


@patch("app.routes.generate_nutrition_tip_with_flash", side_effect=lambda goal: fake_tip())
@patch("app.routes.generate_workout_gemini", side_effect=lambda user: fake_plan())
def test_generate_then_feedback(mock_workout, mock_tip, client):
    payload = {
        "username": "Demo User",
        "user_id": "demo-002",
        "age": 21,
        "weight": 70,
        "goal": "endurance",
        "intensity": "low",
    }

    generated = client.post("/api/generate-workout", json=payload)
    assert generated.status_code == 200

    with patch(
        "app.routes.update_workout_plan",
        side_effect=lambda original_plan, feedback, goal, intensity: fake_plan(),
    ):
        response = client.post(
            "/api/submit-feedback",
            json={
                "user_id": "demo-002",
                "feedback": "Please include more recovery work.",
            },
        )

    assert response.status_code == 200
    assert len(response.json()["updated_plan"]["days"]) == 7
