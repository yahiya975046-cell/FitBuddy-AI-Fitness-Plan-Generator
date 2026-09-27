from google import genai
from google.genai import types

from .config import get_settings
from .schemas import NutritionTip


def _client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to the .env file."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate_nutrition_tip_with_flash(goal: str) -> NutritionTip:
    settings = get_settings()
    client = _client()

    prompt = f"""
Create one concise general nutrition/recovery tip for an educational
wellness application.

Fitness goal: {goal}

Rules:
- Encourage ordinary balanced food, hydration and recovery.
- Do not prescribe a restrictive diet or calorie target.
- Do not recommend supplements or medication.
- Keep the advice practical and concise.
- Return only JSON matching the supplied schema.
"""

    response = client.models.generate_content(
        model=settings.tip_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=NutritionTip,
            temperature=0.3,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty nutrition response.")

    return NutritionTip.model_validate_json(response.text)
