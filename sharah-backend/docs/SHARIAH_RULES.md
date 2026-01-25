# Shariah Rules (Engine Reference)

This document summarizes the **engine** behaviour described in `TECHNICAL_DOCUMENTATION.md`. The **backend** does not implement these rules; the **engine owner** does. It is kept here as reference for them.

## Principles

- **Riba** — Interest on money: Haram.
- **Musharaka** — Profit-sharing partnership: Halal.
- **Murabahah** — Cost-plus markup: Halal.
- **Gharar** — Excessive uncertainty: reduce confidence, flag.

## Rules (for engine implementation)

1. **Interest (Riba)**  
   - `interest_rate > 0` and `profit_sharing_pct == 0` → **Haram**, low confidence.  
   - `interest_rate > 0` and `profit_sharing_pct >= interest_rate` → Potentially Halal.  
   - Otherwise (profit < interest) → Not compliant, medium confidence.

2. **Profit-sharing (Musharaka)**  
   - `interest_rate == 0` and `profit_sharing_pct > 0` → **Halal**, high confidence.

3. **Zero interest, zero profit**  
   - **Murabahah** → Likely Halal. **Other** → Inconclusive; recommend more details.

4. **Gharar**  
   - Short/vague description, penalty-style language → Flag, reduce confidence.

## Output

Engine must return `ShariaCheckResponse`: `is_shariah_compliant`, `confidence`, `reasoning`, `flagged_issues`, `applicable_fatwas`, `recommendation`. See `models/schemas.py` and `TECHNICAL_DOCUMENTATION.md`.
