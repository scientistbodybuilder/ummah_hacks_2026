# SHARAH Backend Testing

## Run Tests

```bash
cd sharah-backend
source .venv/bin/activate
pytest tests/ -v
```

## Layout

- **`tests/test_api.py`** — Integration tests for the API (health, POST /api/shariah-check, validation errors, response time).
- **`tests/conftest.py`** — Path setup, pytest-asyncio.

Engine logic is owned by another team; there are no engine unit tests in this repo.

## Coverage

- **GET /health** — 200, `status: ok`.
- **POST /api/shariah-check** — Valid body → 200, correct response schema.
- **Validation** — Invalid/missing fields, description too short → 422.
- **Performance** — Shariah-check response &lt; 1 s.
- **CORS** — Health check succeeds (CORS configured).

Tests use the engine **stub**; they validate the API layer only.
