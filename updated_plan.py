from google import genai
from google.genai import types

from .config import get_settings
from .schemas import WorkoutPlan


def _client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to the .env file."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def update_workout_plan(
    original_plan: WorkoutPlan,
    feedback: str,
    goal: str,
    intensity: str,
) -> WorkoutPlan:
    settings = get_settings()
    client = _client()

    prompt = f"""
Update the following general-wellness workout plan.

Goal: {goal}
Intensity: {intensity}
User feedback: {feedback}

Original plan:
{original_plan.model_dump_json(indent=2)}

Rules:
- Apply the feedback only where it is safe and reasonable.
- Preserve useful parts of the original plan.
- Keep exactly 7 days.
- Keep recovery/rest.
- Do not add dangerous challenges, starvation, dehydration, medication,
  supplements, or extreme training.
- Return only JSON matching the supplied schema.
"""

    response = client.models.generate_content(
        model=settings.update_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=WorkoutPlan,
            temperature=0.4,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty updated plan.")

    return WorkoutPlan.model_validate_json(response.text)
