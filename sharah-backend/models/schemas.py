"""Pydantic request/response schemas for Shariah compliance API."""

from typing import List

from pydantic import BaseModel, Field


VALID_PRODUCT_TYPES = [
    "revenue-based-advance",
    "musharaka",
    "murabahah",
    "sukuk",
    "bnpl",
    "other",
]


class ShariaCheckRequest(BaseModel):
    """Request body for POST /api/shariah-check."""

    product_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Product type: revenue-based-advance, musharaka, murabahah, sukuk, bnpl, other",
    )
    interest_rate: float = Field(
        ...,
        ge=0,
        le=50,
        description="Annual interest rate (%)",
    )
    profit_sharing_pct: float = Field(
        ...,
        ge=0,
        le=50,
        description="Profit-sharing percentage (%)",
    )
    terms_length_months: int = Field(
        ...,
        ge=1,
        le=120,
        description="Duration of agreement in months",
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Plain text product description",
    )


class ShariaCheckResponse(BaseModel):
    """Response body for POST /api/shariah-check."""

    is_shariah_compliant: bool = Field(
        ...,
        description="True if Halal, false if Haram",
    )
    confidence: float = Field(
        ...,
        ge=0,
        le=100,
        description="0–100% confidence in assessment",
    )
    reasoning: str = Field(
        ...,
        description="Explanation of why Halal/Haram",
    )
    flagged_issues: List[str] = Field(
        default_factory=list,
        description="Specific issues found (empty if compliant)",
    )
    applicable_fatwas: List[str] = Field(
        default_factory=list,
        description="Islamic principles that apply",
    )
    recommendation: str = Field(
        ...,
        description="Next step for user",
    )
