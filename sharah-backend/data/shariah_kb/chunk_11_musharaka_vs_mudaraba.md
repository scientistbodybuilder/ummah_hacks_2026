# Chunk 11: Musharaka vs. Mudaraba — Partnership vs. Mandate Profit-Sharing

## 1-Sentence Rule
**Musharaka** = both parties contribute capital + management; share profit/loss in agreed ratio.  
**Mudaraba** = one party provides capital (Rab-al-Maal), other provides expertise (Mudarib); capital owner bears loss, Mudarib bears opportunity cost.  
**Key**: Both require genuine risk-sharing; guarantees collapse both into loans.

## What to Check
- Who contributes **capital and who contributes labor/expertise**?
- In Musharaka, do **both parties manage the venture**, or is it one-sided?
- In Mudaraba, is the **Mudarib (manager) at personal risk for negligence** (yes = Halal), or insulated from loss?
- Are **profit/loss ratios clearly stated and fair** (not exploitative)?
- Does the contract distinguish between **profit-share** (agreed upfront) vs. **management fee** (separate, based on service)?
- Can the **Rab-al-Maal (capital provider) exit early**, or are they locked in (sign of loan)?
- If the venture **underperforms**, can the manager blame "market risk" (acceptable) or is there **negligence** (manager liable)?
- Is there a **clear accounting and profit-calculation mechanism**, or vague?

## Red Flag Keywords
- Fixed return to capital provider (makes it loan, not partnership)
- Management fee separate from profit-share (acceptable, but must be explicit)
- Capital provider can exit anytime (suggests loan)
- Mudarib (manager) insulated from loss (violates Mudaraba principle)
- Profit-share percentage vague or 'to be determined' (Gharar)
- Capital provider retains control + Mudarib is hired hand (not true Musharaka)

## Questions to Ask If Uncertain
1. **In Musharaka**: Do both parties have **equal say** in major decisions, or is one party dominant?
2. **In Mudaraba**: Is the **Mudarib held accountable for negligence** (e.g., losses from poor management), or do they claim "market risk"?
3. Is the **profit-share ratio fair** given each party's contribution (e.g., 50-50 capital but 70-30 profit would be suspicious)?
4. If the venture generates **zero profit**, does each party accept zero return (true risk-sharing)?
5. Is **actual profit calculated from audited financials**, or estimated/guessed?
6. Can profits be **manipulated** (e.g., inflated costs to reduce reportable profit)?
7. Are there **regular account statements and audits** provided to partners?

## Shariah Status
- **Verdict (Halal)**: Capital + risk-sharing; profit based on actual results; no guarantee
- **Verdict (Haram)**: Fixed return, guarantee, or capital protection; no real risk
- **Verdict (Conditional)**: Profit-share exists but structured with guardrails (e.g., manager fee capped) that approach loan-like behavior; needs scrutiny
- **Confidence Level**: High (AAOIFI Standards 12 & 13 explicit)

## Evidence & Citations
- **AAOIFI Shariah Standard 12 (Musharaka)**: "All partners contribute capital. Profit distributed in agreed ratio; losses borne proportionally to capital contribution or agreed ratio. Both partners share management or delegate to one."
- **AAOIFI Shariah Standard 13 (Mudaraba)**: "Capital provider (Rab-al-Maal) supplies funds. Mudarib (manager) supplies expertise. Losses (capital) borne by Rab-al-Maal. Mudarib liable for negligence/breach."
- **IFSB Core Principles**: "Musharaka and Mudaraba require genuine risk-sharing; any guarantee or fixed return disqualifies the product."
- **Islamic Bankers Center (2024)**: "Many 'Mudaraba' products in Malaysia are structured with implicit guarantees (LOU) or performance floors; these are loan-like and disqualified."
- **Hassan et al. (2020)**: "True Musharaka requires partnership in both profit and loss; accounting transparency is critical."

## SHARAH Engine Use
- **Applicable to**: partnership_like; investment products claiming Musharaka/Mudaraba
- **Confidence impact**: If **genuine profit/loss-sharing, no guarantee, clear accounting** → +25 to +30; if **fixed return or guarantee** → -50
- **Trigger keywords**: ["musharaka", "mudaraba", "partnership", "profit-share", "capital contribution", "management fee"]
- **Sample verdicts**:
  - `IF (profit_sharing_pct > 0) AND (no_guarantee) AND (profit_calculated_from_actual_results) AND (loss_sharing_explicit) THEN principle_tag="musharaka/mudaraba" confidence_adjust="+25" is_halal=true_conditional`
  - `IF ("fixed return" OR guarantee OR "capital protected") THEN issue="Disguised loan; no true risk-sharing" principle_tag="riba" confidence_adjust="-50" is_halal=false`

## Post-MVP LLM Use
- LLM can explain the Musharaka/Mudaraba distinction
- LLM **cannot** approve a guaranteed return as "partnership"
