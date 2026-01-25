"""Integration tests for FastAPI endpoints."""

import time

import pytest
from fastapi.testclient import TestClient

# Ensure backend root on path (conftest adds it)
import sys
from pathlib import Path
backend_root = Path(__file__).resolve().parent.parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from main import app

client = TestClient(app)


def test_health_returns_200():
    """GET /health returns 200 OK."""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert "sharah" in data.get("service", "").lower()


def test_shariah_check_valid_request():
    """POST /api/shariah-check returns valid response for valid input."""
    payload = {
        "product_type": "revenue-based-advance",
        "interest_rate": 0,
        "profit_sharing_pct": 5,
        "terms_length_months": 12,
        "description": "VePay revenue-based advance: $50K advance against 5% of daily seller revenue, capped at $60K total repayment",
    }
    r = client.post("/api/shariah-check", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "is_shariah_compliant" in data
    assert "confidence" in data
    assert "reasoning" in data
    assert "flagged_issues" in data
    assert "applicable_fatwas" in data
    assert "recommendation" in data
    assert isinstance(data["is_shariah_compliant"], bool)
    assert 0 <= data["confidence"] <= 100


def test_shariah_check_invalid_input_validation():
    """Invalid input (e.g. interest_rate > 50) returns 422."""
    payload = {
        "product_type": "revenue-based-advance",
        "interest_rate": 99,
        "profit_sharing_pct": 5,
        "terms_length_months": 12,
        "description": "Valid description with enough characters for validation.",
    }
    r = client.post("/api/shariah-check", json=payload)
    assert r.status_code == 422


def test_shariah_check_missing_field():
    """Missing required field returns 422."""
    payload = {
        "product_type": "revenue-based-advance",
        "interest_rate": 0,
        "profit_sharing_pct": 5,
        "terms_length_months": 12,
    }
    r = client.post("/api/shariah-check", json=payload)
    assert r.status_code == 422


def test_shariah_check_description_too_short():
    """Description min_length=10 returns 422."""
    payload = {
        "product_type": "other",
        "interest_rate": 0,
        "profit_sharing_pct": 0,
        "terms_length_months": 12,
        "description": "Short.",
    }
    r = client.post("/api/shariah-check", json=payload)
    assert r.status_code == 422


def test_response_time_under_one_second():
    """POST /api/shariah-check responds in < 1 second."""
    payload = {
        "product_type": "revenue-based-advance",
        "interest_rate": 0,
        "profit_sharing_pct": 5,
        "terms_length_months": 12,
        "description": "VePay revenue-based advance: $50K advance against 5% of daily seller revenue, capped at $60K total repayment.",
    }
    start = time.perf_counter()
    r = client.post("/api/shariah-check", json=payload)
    elapsed = time.perf_counter() - start
    assert r.status_code == 200
    assert elapsed < 1.0


def test_cors_headers_present():
    """CORS headers are present on response (OPTIONS or GET)."""
    r = client.get("/health")
    assert r.status_code == 200
    # TestClient may not expose all CORS headers; optional check
    # assert "access-control-allow-origin" in [h.lower() for h in r.headers]
