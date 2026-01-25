# Chunk 8: Murabaha (Cost-Plus Sale) — Asset Backing & Disclosure Requirements

## 1-Sentence Rule
Murabaha is Halal **only if**: (1) Bank genuinely **owns and purchases the asset first**, (2) **Cost + profit margin disclosed and agreed upfront**, (3) **Asset transferred to customer** (not collateral), and (4) **Customer bears asset risk**.

## What to Check
- Does contract explicitly state "Bank purchases [asset] at cost ₱X, sells to customer at ₱X + ₱Y profit"?
- Can customer **verify the bank's cost** (invoice/receipt shown) or is cost assertion unverified?
- Is the **profit margin a fixed amount or percentage**, clearly stated, non-negotiable?
- When does **ownership transfer** to customer: at signing, at first payment, or only at final payment (red flag)?
- If the asset **becomes defective**, does the customer have recourse, or does bank disclaim responsibility?
- Is the asset **collateralized to the bank** (bank holds title/lien until final payment), or does customer own it upfront?
- Can customer **freely sell the asset**, or is there a restriction?
- Are **recurring costs** (e.g., property tax, maintenance) the customer's responsibility, or shared?

## Red Flag Keywords
- Cost withheld (bank doesn't disclose original purchase price)
- Profit margin negotiable or subject to credit review (margin should be fixed upfront)
- Bank retains title, lien, security interest (suggests loan, not sale)
- At bank's discretion, margin determined by (vague)
- Customer accepts asset 'as-is' with no recourse (customer bears all risk, but doesn't own—loan-like)
- Installments begin, full ownership transfers only at final payment (indicates loan structure)

## Questions to Ask If Uncertain
1. Can customer see the **bank's original invoice** proving the purchase price ₱X?
2. Is the **profit margin ₱Y disclosed and locked in at signing**, or can it change?
3. If the item is a **car with a defect**, does customer have warranty recourse against the bank?
4. Can customer **immediately** register the asset in their name (e.g., car title, property deed), or must they wait?
5. If customer pays off the loan early, is there a **discount** (good: shows asset ownership), or is it disallowed?
6. If the asset **depreciates in value**, does the customer bear the loss, or does bank adjust the repayment?
7. Does the contract separate the **asset from the financing** (two instruments), or combine them?

## Shariah Status
- **Verdict (Halal)**: Bank owns first, cost + profit disclosed, asset transferred, customer bears risk
- **Verdict (Haram)**: Cost hidden, profit variable, asset not transferred, bank holds title
- **Confidence Level**: Very High (AAOIFI Standard 2 is explicit; but enforcement in practice is weak)

## Evidence & Citations
- **AAOIFI Shariah Standard 2 (Murabaha)**: "Bank must own and take possession of asset before sale. Cost and profit margin must be disclosed and accepted by customer. Ownership transfers to customer."
- **State Bank of Pakistan (2024)**: "Essentials of Murabaha: (1) Bank buys goods; (2) Cost disclosed; (3) Profit margin agreed; (4) Sold to customer; (5) Deferred or immediate payment."
- **BNM Guidelines (Murabaha)**: "Murabaha requires bank ownership; cost disclosure; profit linked to asset, not time. Failure to disclose cost or retaining title invalidates structure."
- **IFSB Core Principles**: "Murabaha revenue is asset-backed profit; not lending income."
- **SSRN Paper (2025)**: "Many banks label products 'Murabaha' but structure as loans; IFRS 9 treatment masks true nature. Transparency requires disclosing actual cost."
- **Trowers & Hamlins (2024)**: "Murabaha: Bank owns asset; sells at cost + agreed profit; customer gets title. Custody/collateral post-sale is acceptable if clearly separated."

## SHARAH Engine Use
- **Applicable to**: sale_like; any "Murabaha" labeled product
- **Confidence impact**: If **cost disclosed + profit stated + asset transferred + customer owns** → +20 to +25; if **cost hidden or title retained** → -35
- **Trigger keywords**: ["Murabaha", "cost-plus", "purchase price", "profit margin", "asset transfer", "ownership", "bank owns first"]
- **Sample verdicts**:
  - `IF product_type == "murabahah" AND cost_disclosed == true AND profit_margin_fixed == true AND asset_transferred == true THEN principle_tag="murabaha" confidence_adjust="+20" is_halal=true_conditional`
  - `IF "Murabaha" label BUT cost_not_disclosed OR "bank retains title" OR profit_margin_variable THEN issue="Murabaha in name only; may be disguised loan" confidence_adjust="-30" is_halal=false_probable`

## Post-MVP LLM Use
- LLM can request: "Show the bank's original invoice"
- LLM **cannot** excuse missing cost disclosure
