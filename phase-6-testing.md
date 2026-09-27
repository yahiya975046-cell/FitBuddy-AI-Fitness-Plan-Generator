# Phase 6 — Testing

## Automated testing

Run:

```bash
pytest -q
```

The test suite mocks Gemini service functions. This keeps unit/integration route tests deterministic and avoids API charges during normal testing.

## Manual testing checklist

### Home

- [ ] Page loads.
- [ ] Form is responsive.
- [ ] All required fields validate.

### Generation

- [ ] Valid data reaches the backend.
- [ ] Gemini returns a structured plan.
- [ ] Exactly seven days display.
- [ ] Nutrition/recovery tip displays.
- [ ] User record is saved.

### Feedback

- [ ] Existing User ID is accepted.
- [ ] Feedback updates the plan.
- [ ] Original plan remains available in database.
- [ ] Updated plan is displayed.

### Admin

- [ ] Wrong key is rejected.
- [ ] Correct key opens dashboard.
- [ ] User data is visible.
- [ ] Original and updated plans can be compared.

### API

- [ ] `/docs` opens.
- [ ] `/api/health` returns 200.
- [ ] Invalid input returns 422.
