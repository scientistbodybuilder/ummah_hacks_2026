"""
Shariah compliance engine service.

This module imports and exposes the engine implementation from the engine package.
"""

from models.schemas import ShariaCheckRequest, ShariaCheckResponse
from engine.shariah_engine import check_shariah_compliance as _check_shariah_compliance


async def check_shariah_compliance(request: ShariaCheckRequest) -> ShariaCheckResponse:
    """
    Run Shariah compliance check on product specification.

    Delegates to the engine implementation in engine.shariah_engine.
    """
    return await _check_shariah_compliance(request)
