# Phase 2 — Requirement Analysis

## Functional requirements

### User

- Enter username.
- Enter user ID.
- Enter age.
- Enter weight.
- Select goal.
- Select intensity.
- Generate a seven-day plan.
- Read nutrition/recovery guidance.
- Submit feedback.
- View revised plan.

### Admin

- Authenticate with an admin key for the educational local demo.
- View all stored users.
- Compare original and updated plans.

### Backend

- FastAPI routes.
- Pydantic validation.
- Gemini integration.
- SQLAlchemy persistence.
- SQLite database.

## Non-functional requirements

- Responsive UI.
- Secrets in `.env`.
- Testable service layer.
- Structured AI responses.
- Useful errors.
- No API key in frontend source.

## Technology

- Python 3.11+
- FastAPI
- Uvicorn
- Jinja2
- SQLAlchemy
- SQLite
- Pydantic
- Google GenAI SDK
- HTML/CSS/JavaScript
