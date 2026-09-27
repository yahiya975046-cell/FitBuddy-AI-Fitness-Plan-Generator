from typing import Literal

from pydantic import BaseModel, Field, field_validator

Goal = Literal[
    "weight loss",
    "muscle gain",
    "general wellness",
    "flexibility",
    "endurance",
]

Intensity = Literal["low", "medium", "high"]


class UserInput(BaseModel):
    username: str = Field(min_length=2, max_length=120)
    user_id: str = Field(min_length=2, max_length=80)
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, le=500)
    goal: Goal
    intensity: Intensity

    @field_validator("username", "user_id")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=2, max_length=80)
    feedback: str = Field(min_length=3, max_length=1000)


class Exercise(BaseModel):
    name: str
    sets: str
    reps_or_duration: str
    rest: str


class WorkoutDay(BaseModel):
    day: str
    focus: str
    warm_up: str
    exercises: list[Exercise]
    cool_down: str


class WorkoutPlan(BaseModel):
    title: str
    overview: str
    days: list[WorkoutDay] = Field(min_length=7, max_length=7)
    safety_note: str


class NutritionTip(BaseModel):
    tip: str
    recovery_note: str
