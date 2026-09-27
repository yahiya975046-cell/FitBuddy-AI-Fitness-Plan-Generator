# Phase 8 — Demonstration

## Recommended demo script

### 1. Introduce the project

Say:

> FitBuddy is an AI-powered fitness plan generator. It collects basic user information, generates a structured seven-day workout plan with Gemini, provides a recovery tip, stores the result, and lets the user revise the plan using feedback.

### 2. Run the application

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

### 3. Generate

Enter a demo profile and click **Generate 7-Day Plan**.

Show:

- profile summary
- seven days
- exercise details
- recovery tip

### 4. Feedback

Enter feedback and click **Update My Plan**.

Explain that the original plan and feedback are sent to the update service and the revised plan is stored.

### 5. Admin

Open:

```text
/view-all-users?admin_key=fitbuddy-demo-admin
```

Show the original and updated plan records.

### 6. API

Open:

```text
/docs
```

Demonstrate the health endpoint and JSON generation endpoint.

### 7. Testing

Run:

```bash
pytest -q
```

Show the passing test result.
