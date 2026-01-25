"""
Shariah compliance engine – STUB.

The engine is implemented by another team. Replace this module (or implement
check_shariah_compliance below) with the real logic.

The API calls:
  result = await check_shariah_compliance(request)
and expects a ShariaCheckResponse. Keep that interface.
"""

from models.schemas import ShariaCheckRequest, ShariaCheckResponse


async def check_shariah_compliance(request: ShariaCheckRequest) -> ShariaCheckResponse:
    """
    Run Shariah compliance check on product specification.

    TODO: Replace with actual engine implementation. This stub returns a
    placeholder so the API remains functional for frontend integration.
    """
    return ShariaCheckResponse(
        is_shariah_compliant=True,
        confidence=0.0,
        reasoning="[Engine stub – implement check_shariah_compliance in services.shariah_engine]",
        flagged_issues=[],
        applicable_fatwas=[],
        recommendation="Replace services.shariah_engine with the real implementation.",
    )
