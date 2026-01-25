# SHARAH Backend

FastAPI **API layer** for SHARAH: Shariah compliance validation for Islamic financial products.

**Scope:** This repo contains only the **backend** (HTTP API, routes, schemas, validation). The **Shariah engine** (compliance logic) and **frontend** are owned by other teams.

## Setup

```bash
cd sharah-backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # optional
```

## Run

```bash
uvicorn main:app --reload
```

- API: **http://localhost:8000**
- OpenAPI docs: **http://localhost:8000/docs**
- Health: **GET http://localhost:8000/health**

## Test

```bash
pytest tests/ -v
```

## API

- **GET /health** — Health check.
- **POST /api/shariah-check** — Validate a product. Body:

```json
{
  "product_type": "revenue-based-advance",
  "interest_rate": 0,
  "profit_sharing_pct": 5,
  "terms_length_months": 12,
  "description": "Plain text product description (min 10 chars)."
}
```

See `TECHNICAL_DOCUMENTATION.md` in the project root for the full API spec.

## Engine integration

The route calls `check_shariah_compliance(request)` in `services/shariah_engine.py`. That module currently contains a **stub** that returns a placeholder response. The **engine owner** should replace it with the real implementation, keeping the same interface:

```python
async def check_shariah_compliance(request: ShariaCheckRequest) -> ShariaCheckResponse
```

Request/response schemas are in `models/schemas.py`. The `data/` folder holds reference files (`fatwas_database.json`, `product_examples.json`) for the engine if needed.

## Docker

```bash
docker build -t sharah-backend .
docker run -p 8000:8000 sharah-backend
```

## Structure

- `main.py` — FastAPI app, CORS, routes.
- `routes/shariah_check.py` — POST /api/shariah-check.
- `services/shariah_engine.py` — **Stub**; engine owner implements logic here.
- `models/schemas.py` — Pydantic request/response.
- `data/` — Reference data for engine (optional).
- `tests/` — API integration tests.
