# Chunk 5: Profit-Sharing vs. Guaranteed Return — Risk-Sharing (Musharaka/Mudaraba)

## 1-Sentence Rule
In genuine Musharaka/Mudaraba, **all partners/investors must share in actual profits AND losses** (including loss of capital); any guarantee of capital or return is Haram and collapses the structure into a hidden loan.

## What to Check
- Does the contract promise a **fixed return** or guaranteed minimum (e.g., "8% guaranteed"), or is return tied to **actual profit/revenue**?
- If a partner/investor loses money, do **all parties lose proportionately**, or does bank/sponsor bear no loss?
- Is there a "Letter of Undertaking" (LOU) or guarantee clause that **protects the investor's capital**?
- Does the contract specify **profit-sharing ratio** (explicit) or is it vague?
- If the underlying business fails, is the investor's capital at risk, or is it "protected"?
- Can the managing partner (Mudarib) take a salary/fee separate from profit-share (red flag if it's fixed instead of incentive-aligned)?
- Is there a **buyback clause** or option to exit with capital intact (violates risk-sharing)?

## Red Flag Keywords
- guaranteed return, minimum interest, fixed dividend
- capital is protected, principal guarantee, no loss of capital
- Letter of Undertaking (bank promises to cover losses)
- buyback clause, exit guarantee, redemption guarantee
- fixed management fee (separate from profit share)
- capped loss, floor return, minimum 5% even if business fails

## Questions to Ask If Uncertain
1. If the underlying asset/business **loses 20% in value**, does the investor's capital shrink by 20%?
2. Is the return **dependent on actual reported profit**, or is it a **fixed percentage regardless of performance**?
3. If the venture fails completely, does investor lose their entire contribution, or is some amount guaranteed?
4. Can the investor **exit early** and get their capital back (usually indicates loan, not partnership)?
5. Is the profit-share ratio **agreed upfront and fixed**, or does the manager take a bonus/commission that reduces investor return?
6. Are profits calculated on **net profit (after costs)** or **gross revenue** (inflates apparent returns)?

## Shariah Status
- **Verdict (Halal)**: Profit + loss sharing; all parties at risk; no guaranteed returns
- **Verdict (Haram)**: Capital guaranteed, return guaranteed, or investor protected while manager bears all risk
- **Confidence Level**: High (AAOIFI and IFSB both reject disguised loans)

## Evidence & Citations
- **AAOIFI Shariah Standard 12 (Musharaka)**: "All partners must share profits AND losses in agreed ratio. Any guarantee of capital or return converts contract into loan (Qard)."
- **AAOIFI Shariah Standard 13 (Mudaraba)**: "Mudarib (manager) must be responsible for losses if due to negligence. Capital provider (Rab-al-Maal) bears losses from market risk. No fixed return allowed."
- **IFSB Core Principles**: "Investment accounts must be structured as true risk-sharing; any capital guarantee disqualifies the product."
- **Islamic Bankers Center (Malaysia) Research**: "Letter of Undertaking (LOU) is key indicator of hidden loan; many banks use LOU to reduce capital charge from 200-400% (true equity) to 50-100% (debt)."
- **Febianto (Cited 21x)**: "Risk management in Mudharabah/Musharaka: capital protection mechanisms (LOU, guarantees) are structurally incompatible with Islamic principles."
- **State Bank Pakistan**: "Musharaka must demonstrate genuine partnership; guarantees invalidate the structure."

## SHARAH Engine Use
- **Applicable to**: partnership_like contracts; investment products; profit-sharing structures
- **Confidence impact**: If **clear profit-sharing, no guarantee, real loss possibility** → +25 to +30; if **guaranteed return or capital protection** → -40 (hard flag)
- **Trigger keywords**: ["guaranteed return", "minimum profit", "capital protected", "fixed dividend", "buyback", "undertaking"]
- **Sample verdicts**:
  - `IF profit_sharing_pct > 0 AND interest_rate == 0 AND "no guarantee" THEN principle_tag="musharaka/mudaraba" confidence_adjust="+25" is_halal=true_conditional`
  - `IF "guaranteed return" OR "capital protected" OR "minimum X% regardless" THEN issue="Hidden loan (capital guarantee violates Musharaka)" principle_tag="riba" confidence_adjust="-40" is_halal=false`

## Post-MVP LLM Use
- LLM can explain the Musharaka/Mudaraba difference
- LLM **cannot** approve a guaranteed return as "partnership"
