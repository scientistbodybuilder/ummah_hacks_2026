# Chunk 6: Revenue-Based Financing (RBF) / Merchant Cash Advance (MCA) — When It Looks Like a Loan

## 1-Sentence Rule
A revenue-based advance is **conditionally Halal only if**:  
1) Repayment is **variable** (tied to daily/monthly revenue, not fixed amount),  
2) No **fixed deadline** (customer pays until cap is reached, e.g., 1.3x advance),  
3) **Buyback clause absent** (bank cannot force repayment if revenue stops), and  
4) **Late fees absent or rare** (no penalty for slow payment).  
If any of these fail, it's a **disguised loan** with riba.

## What to Check
- Is repayment amount **fixed** (e.g., "pay ₱50K total") or **variable** (e.g., "5% of daily sales")?
- Is there a **cap** on total repayment (e.g., "until ₱60K paid," no more required)?
- Is there a **fixed maturity** (e.g., "must be repaid in 12 months") or open-ended until cap?
- Can the bank **force full repayment** before the ₱60K cap (buyback clause)?
- If merchant revenue drops to ₱0, does the obligation **pause/forgive**, or does debt still accrue?
- What happens if the business fails: does merchant owe the full cap or just actual revenue collected?
- Is there a **late fee** if daily/monthly installment is missed, and if so, what triggers it?
- Is the advance **actually paid daily/weekly** based on real revenue (good), or estimated upfront (suspicious)?

## Red Flag Keywords
- fixed repayment amount, total amount due: ₱60K regardless
- must repay within X months, maturity date, deadline
- buyback option, early repayment required, recall if covenant breached
- late fees apply if daily payout < X%, interest accrues if revenue slow
- personal guarantee, collateral required, if business fails, personal liability
- fees charged monthly on outstanding balance (smells like interest)

## Questions to Ask If Uncertain
1. If revenue is ₱0 this month (e.g., seasonal shutdown), does the repayment **pause**, or is it **still due**?
2. Can the bank **demand full repayment immediately** (buyback), or only upon hitting the agreed cap?
3. Is the ₱60K cap truly a **cap** (no more owed), or can it be extended/modified?
4. If the merchant **pays off the cap early**, is there a **discount** (good sign) or **penalty** (red flag)?
5. Is the daily/weekly payout **collected from actual bank deposits** (good sign of real revenue), or estimated/guessed?
6. Are there **late fees based on missed payment targets** (bad; suggests fixed obligation)?
7. Does the advance agreement include a **personal guarantee** from the owner (bad; converts to loan with personal liability)?

## Shariah Status
- **Verdict (Halal)**: Variable repayment, tied to real revenue, open-ended (until cap), no buyback, no fixed deadline
- **Verdict (Conditional/Gray)**: Slight fixed component (e.g., minimum daily draw) if cap and no late fees
- **Verdict (Haram)**: Fixed repayment, fixed deadline, late fees, buyback clause, personal guarantee, or "interest" on balance
- **Confidence Level**: Medium (some scholars accept slight fixes; most reject buyback + late fees)

## Evidence & Citations
- **AAOIFI Shariah Standard 1 & 2**: "Transaction must reflect actual economic activity. Repayment mechanism that does not vary with merchant's revenue is loan-like (Qard) and charges are Riba."
- **IFSB Guidance**: "Revenue-based contracts must tie cash flows to underlying business performance; fixed repayment schedule converts to debt instrument."
- **BNM Research Papers**: "Merchant cash advance structures widely used in Malaysia are often disguised loans; many lack Shariah governance."
- **ISRA Study**: "Fintech RBF products often include fixed caps + buyback clauses, making them materially equivalent to loans."
- **Islamic Bankers Center (2024)**: "True RBF (equity-like) vs. disguised MCA (debt-like) distinction is key Shariah screen."
- **Fundingsouq (UAE Islamic Finance Hub, 2024)**: "RBF is Halal IF no fixed deadline, no buyback, no late fees; otherwise it's a loan."

## SHARAH Engine Use
- **Applicable to**: loan_like with "profit sharing" veneer; merchant/SME finance products
- **Confidence impact**: If **variable repayment, open-ended, no buyback, no late fees** → +20; if **fixed amount + deadline + late fees** → -45 (loan indicator)
- **Trigger keywords**: ["revenue-based", "daily settlement", "fixed repayment", "cap", "maturity", "buyback", "can demand repayment"]
- **Sample verdicts**:
  - `IF "revenue-based advance" AND repayment_variable == true AND no_buyback AND no_fixed_deadline AND no_late_fees THEN principle_tag="musharaka/mudaraba" confidence_adjust="+15" is_halal=true_conditional`
  - `IF repayment_amount == "fixed" OR "must repay ₱60K in 12 months" OR buyback_clause_present THEN issue="RBF disguised as loan; fixed repayment is Riba characteristic" principle_tag="riba" confidence_adjust="-40"`

## Post-MVP LLM Use
- LLM **must NOT approve RBF** with fixed maturity as "variable repayment product"
- LLM must ask: "Is there a buyback clause? A fixed deadline? Late fees?"
