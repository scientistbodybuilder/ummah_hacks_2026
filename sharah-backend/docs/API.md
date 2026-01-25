# SHARAH API

## Base URL

- Local: `http://localhost:8000`
- Production (example): `https://sharah-api.railway.app`

## Endpoints

### GET /health

Health check for monitoring and load balancers.

**Response:** `200 OK`

```json
{ "status": "ok", "service": "sharah-api" }
```

### POST /api/shariah-check

Validate an Islamic financial product for Shariah compliance.

**Request:** `Content-Type: application/json`

| Field | Type | Constraints |
|-------|------|-------------|
| `product_type` | string | 1–50 chars; e.g. revenue-based-advance, musharaka, murabahah, sukuk, bnpl, other |
| `interest_rate` | float | 0–50 |
| `profit_sharing_pct` | float | 0–50 |
| `terms_length_months` | int | 1–120 |
| `description` | string | 10–5000 chars |

**Response:** `200 OK`

| Field | Type |
|-------|------|
| `is_shariah_compliant` | boolean |
| `confidence` | float (0–100) |
| `reasoning` | string |
| `flagged_issues` | string[] |
| `applicable_fatwas` | string[] |
| `recommendation` | string |

**Errors:** `400` (bad input), `422` (validation), `500` (server error).

See `TECHNICAL_DOCUMENTATION.md` in the project root for examples.
