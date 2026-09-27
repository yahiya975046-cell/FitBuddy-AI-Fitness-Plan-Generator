from google import genai
from google.genai import types

from .config import get_settings
from .schemas import UserInput, WorkoutPlan

SYSTEM_RULES = """
You are the fitness-planning component of an educational wellness application.
Create conservative, general-wellness guidance, not medical treatment.
Do not diagnose conditions.
Do not prescribe medication or supplements.
Do not encourage starvation, purging, dehydration, dangerous challenges,
or extreme exercise.
Use ordinary bodyweight or gym movements with clear recovery.
Do not promise a particular weight-loss or muscle-gain result.
If a medical concern is apparent, recommend appropriate professional guidance.
"""


def _client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to the .env file."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate_workout_gemini(user: UserInput) -> WorkoutPlan:
    settings = get_settings()
    client = _client()

    prompt = f"""
{SYSTEM_RULES}

Create a personalized 7-day workout plan from:
- Name: {user.username}
- Age: {user.age}
- Weight in kg: {user.weight}
- Goal: {user.goal}
- Preferred intensity: {user.intensity}

Requirements:
- Exactly 7 days.
- Every day needs a focus, warm-up, exercises and cooldown/recovery.
- Each exercise needs name, sets, reps or duration, and rest.
- Include sensible recovery/rest days.
- Keep instructions clear for a general user.
- Do not give calorie targets.
- Return only JSON matching the supplied schema.
"""

    response = client.models.generate_content(
        model=settings.workout_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=WorkoutPlan,
            temperature=0.4,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty workout response.")

    return WorkoutPlan.model_validate_json(response.text)
