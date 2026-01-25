# Chunk 7: BNPL (Buy Now Pay Later) — Late Fees & Gharar in Modern Fintech
Keywords: bnpl, buy now pay later, installment, installment plan, no interest, interest-free, 0% interest, late fee, penalty, installment with interest, installment plan with interest, deferred payment, bai muajjal, deferred sale, late payment, penalty, late charge, penalty charge, interest-free period, installment plan

## 1-Sentence Rule
BNPL is **conditionally Halal if structured as cost-plus Murabaha** (bank buys, customer gets immediate possession, fixed price, NO interest), but **Haram if late fees profit the lender or terms are vague** (Gharar).

## What to Check
- Is BNPL structured as **Bai Muajjal** (deferred payment sale) with **zero interest during installments**?
- Does the customer get **immediate possession** of goods/services?
- Is the **sale price = cost + merchant commission only** (Halal), or does it include interest/fees from customer?
- Are **late/penalty fees completely absent** (ideal), cost-based (Ta'widh; acceptable), or profit-based (Haram)?
- If late fees exist, do **excess fees go to charity** (Gharamah treatment; acceptable) or to BNPL provider's profit?
- Are **T&Cs clearly disclosed** (esp. late fees, penalty mechanics, payment schedule) or vague?
- Is the BNPL provider taking a **merchant commission** (Halal) or **charging the customer interest**?
- Does the app encourage **unplanned consumption** (Maysir element; ethical concern)?

## Red Flag Keywords
- late payment fee: X%, overdue charge, penalty APR
- terms subject to change, see terms, charges apply (without disclosure)
- up to X% late charge (no formula disclosed)
- interest-free marketing **but** late fees are compounding or excessive
- installment with interest, cost of deferral
- automatic enrollment, encourage spending, unlimited shopping

## Questions to Ask If Uncertain
1. If customer pays on Day 1, is there **zero additional cost** beyond the sale price?
2. How much do late fees **actually cost** a customer? Is this disclosed upfront?
3. Does the contract allow the BNPL provider to **modify fee structure retroactively**?
4. If customer disputes a charge, is there a **straightforward refund process**?
5. Does the app **interface with predatory behavior** (e.g., "swipe to pay later" with no warnings)?
6. Are terms available **in full clarity in the contract**, or only a summary?
7. Is the merchant subsidizing the BNPL (merchant pays commission, customer gets 0% interest) or does customer bear the cost?

## Shariah Status
- **Verdict (Halal - Ideal)**: Murabaha structure, zero interest, immediate possession, no late fees
- **Verdict (Conditional - Acceptable)**: Zero interest, cost-based late fees only, clear T&Cs, excess fees to charity
- **Verdict (Haram - Common)**: Late fees are interest-equivalent, terms are vague, provider profits from delays
- **Confidence Level**: High (Malaysia BNM, OIC Fiqh Academy have clear guidance; most BNPL apps flagged as non-compliant)

## Evidence & Citations
- **BNM BNPL Guidance (2024)**: "Buy Now Pay Later products must be structured as Bai Muajjal (deferred sale). Late payment charges are only permitted if they reflect **actual administrative costs**. Charges exceeding costs must be **donated to charitable organizations**."
- **Malaysia SAC Resolution (2024)**: "BNPL providers must comply with Ta'widh/Gharamah principles. Shopee PayLater complies (clear fees, excess donated); Atome and others do not."
- **BNM Policy on Affordability**: "BNPL platforms must assess customer ability to repay; 'encourage spending' messaging is unethical."
- **RSSIS Journal (2025)**: "BNPL in Malaysia: Only Shopee meets Shariah compliance; Atome/others flagged for Gharar (vague T&Cs) + Riba (late fee structure)."
- **Islamic Finance Singapore FAQ**: "Atome's late fees constitute 'Riba al-Qard' because they profit the company from delays; no charitable excess distribution mentioned."
- **Fundingsouq (2024)**: "BNPL is Halal only if: (1) Murabaha structure, (2) zero interest, (3) clear penalties, (4) excess fees to charity."

## SHARAH Engine Use
- **Applicable to**: sale_like (BNPL is Murabaha); any installment/deferred payment
- **Confidence impact**: If **zero interest + cost-based or no late fees + clear T&Cs** → +18; if **late fees unclear or excess retained** → -25; if **vague T&Cs** → -15
- **Trigger keywords**: ["BNPL", "buy now pay later", "installment", "late fee", "penalty", "interest-free period", "deferred payment"]
- **Sample verdicts**:
  - `IF product_type == "bnpl" AND interest_rate == 0 AND late_fees == "cost-based or absent" AND TnC_clear == true THEN principle_tag="murabaha" confidence_adjust="+15" is_halal=true_conditional`
  - `IF "BNPL" AND (late_fees unclear OR "up to X%" OR excess_not_to_charity) THEN issue="Gharar (vague penalties) or Riba (excess retained)" confidence_adjust="-20"`

## Post-MVP LLM Use
- LLM can explain Murabaha structure vs. disguised interest
- LLM can check if late fees "make sense" given actual costs
- LLM **must** flag if excess fees don't go to charity
