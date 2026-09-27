# Phase 5 — Development

## Backend

`app/main.py` creates the FastAPI application.

`app/routes.py` connects the UI/API to the AI and database layers.

`app/schemas.py` validates incoming data and defines AI output structures.

`app/models.py` defines the SQLite user record.

`app/database.py` initializes SQLAlchemy.

## Gemini integration

`gemini_generator.py` creates the structured seven-day workout.

`gemini_flash_generator.py` creates a concise nutrition/recovery tip.

`updated_plan.py` uses the original plan plus feedback to produce a revised plan.

## Frontend

- `index.html` collects input.
- `result.html` displays the generated plan and feedback form.
- `all_users.html` displays stored records.
- `error.html` gives a simple failure screen.
- `style.css` provides responsive visual design.
- `app.js` provides a submission/loading state.

## Database

The first application start creates `fitbuddy.db` automatically through SQLAlchemy.
