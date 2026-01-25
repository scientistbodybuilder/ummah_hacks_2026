# Chunk 10: Gharar in Product Description — Vague Terms & Missing Details
Keywords: gharar, vague, terms apply, details subject to change, terms subject to change, conditions apply, conditions subject to change, at discretion, at bank's discretion, as mutually agreed, to be agreed, to be determined, up to, estimated, standard terms, market practice, customary charges, details not disclosed, information not disclosed

## 1-Sentence Rule
If essential contract terms (cost, profit, risk, penalty, payment schedule, asset details, obligations) are **not clearly stated, not quantifiable, or left to future agreement**, the contract has **Gharar** and is Haram, regardless of profit-sharing or asset mentions.

## What to Check
- Can the customer **calculate total cost** from the contract alone, or must they "see T&Cs"?
- Are all **numbers explicit** (price, profit margin, payment amounts, late fees), or are there ranges/percentages without detail?
- Does the contract **reference external documents** without full disclosure (e.g., "see website for fees")?
- Is **risk allocation clear**: who owns the asset, who bears loss, who is liable if delivery fails?
- If the product is Murabaha, is the **asset clearly described** (e.g., "iPhone 15 Pro, 128GB, black, serial ___"), or vague ("a smartphone")?
- If the product is Musharaka, is the **profit-share formula documented** (e.g., "60% to bank, 40% to entrepreneur"), or vague?
- Are **payment dates/amounts explicit** (e.g., "payment of ₱1,500 on 15th of each month"), or flexible ("installments to be determined")?
- Is there a **glossary or definition of terms** (good), or undefined jargon (bad)?

## Red Flag Keywords
- See terms and conditions, terms available online, details subject to change
- Subject to approval, at the bank's discretion, subject to credit review
- As mutually agreed, to be determined, subject to adjustment
- May vary, up to, approximately, estimated
- Standard market terms, industry practice, customary charges
- Vague asset description: a property, goods, inventory (no specifics)

## Questions to Ask If Uncertain
1. If I **close the contract document right now**, can I answer these questions? Cost? Profit? Payment dates? Penalties?
2. Are **all references to T&Cs and external documents fully attached and readable** in the main contract?
3. If the bank **modifies a term** (fee, penalty, payment schedule), is customer consent required?
4. Is there a **glossary explaining key terms** (Murabaha, Musharaka, Gharar)?
5. If a clause is unclear, who **bears the cost of ambiguity**: the bank or the customer?
6. Does the contract **expressly allow unilateral changes**, or is modification prohibited without consent?
7. Is the contract **in the customer's native language**, or is translation provided?

## Shariah Status
- **Verdict (Haram)**: Essential terms missing, vague, or left to future agreement; contract is unenforceable
- **Verdict (Conditional)**: Terms are quantifiable but T&Cs are long/complex; risk if disclosure is insufficient
- **Verdict (Halal)**: All material terms explicit, customer can calculate obligations, T&Cs are clear
- **Confidence Level**: High (AAOIFI Standard 2 explicit; Malaysia SAC enforces this in BNPL cases)

## Evidence & Citations
- **AAOIFI Shariah Standard 2**: "Gharar exists when essential contract terms cannot be ascertained. Such contracts are void."
- **BNM Guidelines (Murabaha, BNPL)**: "Contracts must clearly disclose cost, profit, penalties, payment schedule upfront. References to T&Cs without full disclosure constitute Gharar."
- **Malaysia SAC Decision (Atome BNPL)**: "Late fee amount not disclosed upfront; referred to T&Cs = Gharar. Non-compliant."
- **Malaysia SAC Decision (Shopee PayLater)**: "Fees clearly stated, T&Cs fully disclosed, late fees transparent with charity clause = Compliant."
- **RSSIS Journal (2025)**: "Vague terms in BNPL contracts (e.g., 'fees may apply,' 'charges subject to change') are Gharar flags."
- **Islamic Finance Singapore FAQ**: "Atome: 'Charges apply' without clear formula = Gharar. Prohibited."

## SHARAH Engine Use
- **Applicable to**: all contracts (catches structural Gharar before deep-dive Riba/late-fee analysis)
- **Confidence impact**: If **all terms explicit + T&Cs clear** → no penalty; if **vague/deferred** → -15 to -20
- **Trigger keywords**: ["vague", "subject to", "at discretion", "to be agreed", "see T&C", "charges apply", "may vary", "approximately"]
- **Sample verdicts**:
  - `IF any_essential_term_missing OR "see T&C without disclosure" OR "subject to change" THEN issue="Gharar (vague/missing terms)" principle_tag="gharar" confidence_adjust="-15"`
  - `IF cost_explicit AND profit_explicit AND payment_schedule_explicit AND asset_described AND risk_clear THEN no_gharar_flag`

## Post-MVP LLM Use
- LLM **must** flag vague T&Cs as Gharar
- LLM can ask: "Where are the full T&Cs disclosed?"
