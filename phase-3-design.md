# Phase 3 — Project Design

## Component design

```text
templates/index.html
        │
        ▼
POST /generate-workout
        │
        ├── UserInput validation
        ├── Gemini workout generator
        ├── Gemini nutrition generator
        └── SQLAlchemy / SQLite
                    │
                    ▼
             result.html
                    │
                    ▼
          POST /submit-feedback
                    │
                    ▼
            Gemini update layer
                    │
                    ▼
             updated_plan
```

## Data model

`users` table:

- id
- user_id
- username
- age
- weight
- goal
- intensity
- original_plan
- updated_plan
- nutrition_tip
- created_at
- updated_at

## AI model responsibilities

- Pro-capability configurable model: structured workout generation and feedback updates.
- Flash-capability configurable model: quick nutrition/recovery tip.

The actual model IDs are environment variables rather than hard-coded architectural assumptions.

## Security design

- API key is server-side only.
- `.env` is ignored by Git.
- Admin route requires a configured local demo key.
- User input is validated before AI/database processing.
