# Chunk 2: Gharar (Excessive Uncertainty) — What Vagueness Kills Contracts
Keywords: gharar, uncertainty, vague, subject to, up to, at discretion, terms may vary, unclear, ambiguous, see terms, terms apply, conditions apply, conditions subject to change

## 1-Sentence Rule
A contract is Haram if essential terms (price, delivery, quantity, risk allocation, penalties, fees, obligations) are **unclear, ambiguous, or unknowable** to one or both parties at the time of agreement.

## What to Check
- Are all material terms (price, quantity, delivery date, payment schedule, risk) clearly stated upfront?
- Can the customer calculate **exactly** what they will owe at each stage?
- Are penalty/late fee amounts either absent, vague ("up to X%"), or calculated retroactively?
- Does the contract lack clarity on **who bears risk** if delivery/payment fails?
- Are conditions for early termination, buyback, or changes undefined?
- Is there ambiguity about the **underlying asset** (in Murabaha) or **profit share mechanics** (in Musharaka)?
- Does the term sheet use conditional language ("may," "might," "if applicable") for mandatory fees?

## Red Flag Keywords
- subject to, up to X% (without explicit cap or formula)
- at the bank's discretion, terms may vary, fees subject to change
- as determined by, to be agreed, penalty charges apply (no amount specified)
- unclear payment schedule, variable terms, fluctuating charges
- conditions apply, see terms and conditions (without clear disclosure in contract)
- Missing details: cost of asset, profit margin, payment timeline, risk allocation

## Questions to Ask If Uncertain
1. If I (the customer) read this contract alone, could I calculate my total obligation within ±5%?
2. Are the late fees a fixed amount or percentage? Can they compound?
3. Does the contract explicitly state who owns the asset before full payment?
4. If the financier fails to deliver the asset, what is the customer's recourse?
5. Are early payment discounts clearly offered, or is prepayment forbidden?
6. Is the profit-share (in Musharaka) calculated on net profit, gross revenue, or a fixed percentage—and is formula stated?

## Shariah Status
- **Verdict**: Haram (Gharar in essential terms)
- **Confidence Level**: High (though some gharar is tolerated if benefit > harm; degree varies by scholar)

## Evidence & Citations
- **Hadith (Sahih Muslim)**: "Messenger forbids sales involving gharar"
- **AAOIFI Shariah Standard 2**: Gharar defined as "unascertainable risk or uncertainty affecting essential contract terms"
- **BNM Guidelines (2024)**: "BNPL late payment charges must be clearly defined; vague penalties constitute Gharar"
- **Malaysia SAC Ruling**: Ambiguous late fees = Gharar; "See T&Cs" without disclosure = Gharar
- **Islamic Finance Singapore FAQ**: Atome's late fees flagged as Gharar (no clear formula)
- **ISRA Research**: "Product descriptions must include exact cost, profit, and risk allocation; marketing alone is insufficient"

## SHARAH Engine Use
- **Applicable to**: all contract types (sale_like, partnership_like, loan_like)
- **Confidence impact**: If detected → -10 to -20 (medium penalty; not disqualifying alone, but compounds other issues)
- **Trigger keywords**: ["uncertain", "vague", "up to", "subject to", "may vary", "terms apply", "discretion"]
- **Sample verdicts**:
  - `IF description is vague OR missing cost/price/profit_margin OR "up to X% fee" (unspecified) THEN issue="Gharar (uncertainty)" principle_tag="gharar" confidence_adjust="-15"`
  - `IF late_fees mentioned BUT late_fee_amount NOT specified THEN issue="Gharar (penalty amount unclear)" principle_tag="gharar" confidence_adjust="-10"`

## Post-MVP LLM Use
- LLM can ask: "Can you clarify the exact cost, profit margin, and risk allocation?"
- LLM **forbidden** to ignore missing T&Cs or say "standard market practice is assumed"
