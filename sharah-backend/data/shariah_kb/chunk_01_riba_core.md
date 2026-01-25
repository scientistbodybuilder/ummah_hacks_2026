# Chunk 1: Riba (Interest Prohibition) — Core Definition

Keywords: riba, interest, apr, compound interest, fixed repayment, loan, qard, principal, lending, interest rate, accrued, charge, interest-bearing, business loan, term loan, credit facility, annual interest, monthly interest, financing cost



## 1-Sentence Rule
Any premium charged on money (qard) — whether called "interest," "fee," "charges," or "profit" — is strictly Haram unless structurally decoupled from the debt itself (e.g., profit from asset sale, not loan).

## What to Check
- Is there a loan of money with any amount repaid above principal?
- Is the "interest" fixed or variable, charged per time period or upfront?
- Is the excess justified by the creditor's **real economic activity** (e.g., purchase of asset) or is it pure lending?
- Are interest and profit explicitly conflated (e.g., "10% per annum interest on loan")?
- Is there **time-value-of-money markup** in a sale (Murabaha) vs. a loan (Qard)?
- Is the contract labeled as "fee," "commission," "administrative charge," but functions as interest?

## Red Flag Keywords
- interest, APR, annual percentage rate, compound interest, accrued interest
- fixed repayment, installment plan with interest, monthly charges on principal
- interest accrues, late interest, penalty interest
- rate per annum, basis points, spread
- credit line, revolving credit, interest-bearing deposit

## Questions to Ask If Uncertain
1. Is the financier's profit earned from **possessing and selling an asset** (Halal) or purely from **extending credit over time** (Haram if charged as interest)?
2. Would the creditor make any income if the borrower repaid on day 1?
3. Is the excess amount disclosed upfront and agreed, or calculated retroactively based on time/delay?
4. Does the creditor own the underlying good, or only the debt claim?
5. Is there **shared risk** if the borrower's business fails, or does creditor recover full amount regardless?

## Shariah Status
- **Verdict**: Haram (Fixed interest on any loan of money)
- **Confidence Level**: Very High (unanimous across all madhabs; Quranic foundation)

## Evidence & Citations
- **Qur'an 2:275–276**: "Allah has forbidden interest (riba) and permitted sale (bay')"
- **AAOIFI Shariah Standard 1**: Riba is "any excess over the original amount of a loan"
- **State Bank of Pakistan (2024)**: "Riba encompasses all interest on loans, regardless of form or purpose"
- **OIC Fiqh Academy**: Consensus that interest on money is prohibited in all forms
- **IFSB Core Principles (IFSB-17)**: Banks must ensure all revenue is "asset-backed" or "service-based," never pure lending charges

## SHARAH Engine Use
- **Applicable to**: loan_like, any contract with debt element
- **Confidence impact**: If detected with high certainty → -50 to -80 (depends on severity); if interest_rate > 0 AND profit_sharing_pct == 0 → Flag "Riba risk" immediately
- **Trigger keywords**: ["interest", "APR", "annual rate", "fixed repayment", "accrues"]
- **Sample verdicts**:
  - `IF interest_rate > 0 AND profit_sharing_pct == 0 THEN issue="Riba detected (fixed interest on loan)" principle_tag="riba" confidence_adjust="-50" is_halal=false`
  - `IF description contains ("interest accrues" OR "compound interest" OR "APR") AND interest_rate > 0 THEN is_halal=false reason="Pure interest-based loan"`

## Post-MVP LLM Use
- LLM **forbidden** to override this verdict or say "maybe riba is OK if..."
- LLM **allowed** to ask: "Is the excess compensating for an asset sale (Murabaha) or purely time-based?"
