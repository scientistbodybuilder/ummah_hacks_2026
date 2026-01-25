"""POST /api/shariah-check endpoint."""

import logging

from fastapi import APIRouter, HTTPException

from models.schemas import ShariaCheckRequest, ShariaCheckResponse
from services.shariah_engine import check_shariah_compliance

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["shariah"])


@router.post("/shariah-check", response_model=ShariaCheckResponse)
async def shariah_check(request: ShariaCheckRequest) -> ShariaCheckResponse:
    """
    Validate Islamic financial product for Shariah compliance.
    Returns compliance assessment with confidence, reasoning, and recommendations.
    """
    try:
        result = await check_shariah_compliance(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error in shariah_check: %s", e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error processing request",
        )
