# Chunk 3: Riba vs. Murabaha Profit — Asset Sale (Halal) vs. Pure Loan (Haram)
Keywords: riba, murabaha, asset sale, profit margin, cost plus, markup, purchase price, ownership, title transfer, asset transfer, bank purchases, bank sells, qard, loan-like, interest disguised as sale

## 1-Sentence Rule
The **same monetary return** can be Halal (if from asset sale with disclosed cost + profit margin) or Haram (if from pure lending), depending entirely on whether the financier **owns and transfers an asset** or merely extends credit.

## What to Check
- Does the contract explicitly state "Bank purchases asset, then sells to customer"?
- Is the asset **owned by the bank before transfer to customer**, or does customer receive a loan to buy from a third party?
- Is the cost of the asset disclosed to the customer upfront (Murabaha) or hidden (suspicious)?
- Can the customer take possession/ownership of the asset immediately (or on agreed date)?
- If contract is called a "sale," do property rights actually transfer, or does bank retain title until full payment (risk sign)?
- Is the profit margin a **fixed percentage of cost** (good sign) or **time-based interest** (bad sign)?
- Can the markup be clearly separated from the principal cost?

## Red Flag Keywords
- loan, lending, advance, credit facility + markup or fee
- financing, monthly interest, cost of borrowing
- Asset sale language **but** customer never takes physical/legal possession
- Murabaha label **without** disclosure of purchase cost
- Profit margin: [X%] applied **per month/year** (time-indexed) rather than upfront lump sum
- Bank retains title until (risk: bank doesn't truly transfer asset)

## Questions to Ask If Uncertain
1. Who is buying the asset first: the bank or the customer?
2. Can the customer see the bank's original purchase invoice (cost proof)?
3. Does customer own/control the asset, or is it collateral for a loan?
4. If customer wants to resell the asset early, can they, or does bank prevent it?
5. Is the financier's profit contingent on **actual asset handover**, or does the customer owe it even if asset delivery fails?
6. Is the markup labeled "profit margin" (Halal) or "interest" (Haram)?

## Shariah Status
- **Verdict (Halal)**: If asset is purchased by bank first, cost + profit disclosed upfront, asset transferred to customer
- **Verdict (Haram)**: If labeled "sale" but functions as pure lending with interest markup
- **Confidence Level**: High (rule is clear; enforcement is where abuse happens)

## Evidence & Citations
- **AAOIFI Shariah Standard 2 (Murabaha)**: "Bank must own asset before sale; cost and profit must be disclosed and agreed upfront"
- **State Bank Pakistan Essentials**: "Murabaha = sale with agreed profit margin; not a loan"
- **IFSB Core Principles**: "Revenue from asset transactions (Murabaha, Ijarah) is Halal; revenue from pure lending is Haram"
- **Malaysia BNM Guidance**: "Murabaha-labeled products must involve actual bank ownership; profit linked to asset, not time"
- **Zulkifli Hasan (2024)**: "Many BNPL products use Murabaha label but structure as hidden loans; courts increasingly reject these"
- **SSRN Paper (2025)**: "IFRS 9 treatment of Islamic contracts masks true nature; many products 'disguise riba as asset sales'"

## SHARAH Engine Use
- **Applicable to**: sale_like contracts; any structure claiming Murabaha
- **Confidence impact**: If **clearly asset-backed** → +15 to +25; if **ambiguous ownership** → -20; if **interest-like pricing** → -40
- **Trigger keywords**: ["Murabaha", "cost plus", "asset sale", "purchase price", "profit margin", "ownership", "title transfer"]
- **Sample verdicts**:
  - `IF product_type == "murabahah" AND cost_disclosed == true AND asset_transfer_clear == true THEN principle_tag="murabaha" confidence_adjust="+20" is_halal=true_conditional`
  - `IF "sale" label BUT customer receives loan (not asset) AND "profit margin" is monthly interest THEN issue="Riba disguised as Murabaha" principle_tag="riba" confidence_adjust="-40" is_halal=false`

## Post-MVP LLM Use
- LLM can ask: "Can you show the bank's purchase invoice? When does customer take ownership?"
- LLM **cannot** say "close enough—assume it's a sale" without proof
