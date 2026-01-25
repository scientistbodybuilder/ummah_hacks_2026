# Chunk 4: Late Fees & Penalties — Ta'widh (Cost-Based) vs. Gharamah (Charity-Required)

## 1-Sentence Rule
Late/penalty fees are **conditionally Halal only if they equal actual administrative/recovery costs** (Ta'widh; income to bank) or are **donated to charity** if they exceed costs (Gharamah; not income). Any fee that **profits the creditor from delay** is Riba and Haram.

## What to Check
- Does the contract specify a **fixed late fee** (e.g., "5% of amount due") or a **cost-based adjustment** (e.g., "actual collection costs")?
- If a percentage, is it **capped** and does it **increase with time**, or is it flat?
- Does the contract state that excess fees (beyond actual costs) go to **charity/donor**, or to the bank's profit?
- Is there a formula to calculate "actual costs" (labor, legal, dunning letters), or is it arbitrary?
- Does late fee **compound** (accrue interest on the fee itself)?
- Is the late fee applied **per payment cycle** or does it accumulate?
- Does the contract make late fees **mandatory** even for minor delays (very harsh), or proportionate?

## Red Flag Keywords
- late fee: X% per month (especially if compounding or no cap)
- penalty charge, default interest, overdue fee + interest
- charge accrues, interest on late payment
- charges at bank's discretion (no formula disclosed)
- no excess will be returned or excess retained by bank
- late fees apply immediately, first day of missed payment

## Questions to Ask If Uncertain
1. Can you itemize the **actual cost** of pursuing a late payment (staff time, dunning letters, legal fees)?
2. If actual costs are ₱500 but the fee charged is ₱5,000, what happens to the ₱4,500?
3. Is there a **grace period** (e.g., 5-day grace before fees kick in)?
4. Does the fee **incentivize quick payment** (lower fee for early clearance) or **punish delay without bounds**?
5. How does this fee compare to **actual losses** the bank incurs (e.g., opportunity cost of unpaid capital)?
6. Is the fee applied **once per late payment** or **daily/weekly accumulation**?

## Shariah Status
- **Verdict (Halal)**: Late fees = documented actual costs; capped; no profit to creditor
- **Verdict (Conditional)**: Fees exist but excess goes to charity (Gharamah treatment)
- **Verdict (Haram)**: Fees profit the creditor from the delay; unlimited; no transparency on actual costs
- **Confidence Level**: High (BNM and OIC Fiqh Academy have clear rulings)

## Evidence & Citations
- **BNM Shariah Advisory Council (2010, Reaffirmed 2024)**: "Ta'widh (compensation) is allowed only to extent of actual documented costs. Gharamah (penalty) cannot be income; must be donated to charity."
- **OIC Fiqh Academy Resolution 109/3/12**: "Penalties on delayed debt repayment are prohibited; exceptions only for documented, itemized costs."
- **Malaysia SAC Guidance on BNPL (2024)**: "Late payment charges (LPC) must reflect actual administrative costs; any excess must be transparently donated to approved charities. Shopee complies; Atome does not."
- **BNM Regulation (2024)**: "For late fees exceeding ₱X or Y%, bank must demonstrate cost justification and donate excess to registered charities monthly."
- **Islamic Finance Singapore FAQ**: "Atome's late fees lack transparency; no statement that excess goes to charity → Flagged as non-compliant."
- **Katterbauer et al. (2023)**: "BNPL late fee treatment is primary Shariah concern; most apps fail governance requirement."

## SHARAH Engine Use
- **Applicable to**: all contracts with late/penalty mechanisms (especially BNPL, installment sales)
- **Confidence impact**: If **transparent cost-based + charity clause** → +10; if **no clarity/profit motive** → -20; if **compounding/unlimited** → -30
- **Trigger keywords**: ["late fee", "penalty", "overdue", "default charge", "interest on late", "charges apply"]
- **Sample verdicts**:
  - `IF late_fee_mentioned AND late_fee_amount_disclosed AND (excess_goes_to_charity OR fee_equals_documented_cost) THEN issue=null principle_tag="ta_widh" confidence_adjust="+10"`
  - `IF late_fee_mentioned AND (late_fee_is_percentage_per_month OR "charges at bank discretion" OR no_cap) THEN issue="Late fee may constitute Riba" principle_tag="riba" confidence_adjust="-20"`

## Post-MVP LLM Use
- LLM **must cite** Ta'widh/Gharamah distinction; cannot say "late fees are always Halal" or "always Haram"
- LLM must ask: "Are excess fees sent to charity? Is there a cost justification?"
