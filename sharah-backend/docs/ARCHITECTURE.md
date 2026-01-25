# SHARAH Backend Architecture

## Overview

The backend is the **API layer only**: stateless FastAPI service, request validation, and routing. The **Shariah engine** (compliance logic) is implemented by another team; this repo provides a stub in `services/shariah_engine.py` that they replace.

## Layers

1. **API (routes)** — HTTP handling, Pydantic validation, error responses.
2. **Engine (services)** — **Stub** today; engine owner implements `check_shariah_compliance(request) -> ShariaCheckResponse`.
3. **Data** — `data/` holds reference files (e.g. fatwas, examples) for the engine; no DB in MVP.

## Flow

```
POST /api/shariah-check
  → Pydantic validates body (ShariaCheckRequest)
  → check_shariah_compliance(request)  [engine – stub or real]
  → ShariaCheckResponse (JSON)
```

## Key Files

- `main.py` — App, CORS, router mount.
- `routes/shariah_check.py` — Single route; delegates to engine.
- `services/shariah_engine.py` — Stub; engine owner replaces with real logic.
- `models/schemas.py` — Request/response contracts.

## Design

- **Stateless** — No server-side session.
- **Backend = API only** — Engine and frontend are separate ownership.
