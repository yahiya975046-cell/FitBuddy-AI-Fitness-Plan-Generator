from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseModel):
    app_name: str = Field(default=os.getenv("APP_NAME", "FitBuddy"))
    gemini_api_key: str = Field(default=os.getenv("GEMINI_API_KEY", ""))
    workout_model: str = Field(
        default=os.getenv("GEMINI_WORKOUT_MODEL", "gemini-2.5-pro")
    )
    tip_model: str = Field(
        default=os.getenv("GEMINI_TIP_MODEL", "gemini-2.5-flash")
    )
    update_model: str = Field(
        default=os.getenv("GEMINI_UPDATE_MODEL", "gemini-2.5-pro")
    )
    database_url: str = Field(
        default=os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")
    )
    admin_key: str = Field(
        default=os.getenv("ADMIN_KEY", "fitbuddy-demo-admin")
    )
    debug: bool = Field(
        default=os.getenv("DEBUG", "true").lower() == "true"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
