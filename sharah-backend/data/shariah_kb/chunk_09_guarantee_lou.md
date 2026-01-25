# Chunk 9: Guarantee Clauses & Letters of Undertaking — Red Flags in Musharaka/Mudaraba

## 1-Sentence Rule
Any **guarantee of capital** (by bank/sponsor) in Musharaka/Mudaraba **automatically converts the contract into a hidden loan** (Qard); investor no longer bears risk, so profit-share is riba (interest), not partnership.

## What to Check
- Is there a "Letter of Undertaking" (LOU) or guarantee clause stating the bank will cover investor losses?
- Does the contract promise "capital is protected," "principal guaranteed," "minimum return X%"?
- If the underlying business/venture **loses 30% of value**, does the investor's capital **shrink by 30%** (risk-sharing), or is some amount "protected"?
- Is there a **buyback guarantee** (investor can exit with capital intact on demand)?
- Does the contract include a **floor return** (e.g., "guaranteed 5% even if business fails")?
- Is the manager/bank **absolved of loss responsibility** while investor bears all downside?
- Can the investor **demand return of capital early** (suggests loan, not partnership)?
- Are there **covenants/ratios** that trigger bank intervention if breached (suggests debt, not equity)?

## Red Flag Keywords
- Letter of Undertaking, LOU, guarantee, guaranteed return
- capital is protected, principal guarantee, loss coverage
- buyback option, redemption guarantee, exit guarantee
- floor return, minimum X%, guaranteed dividend
- call option (investor can exit at face value)
- subordinated, mezzanine (suggests hybrid debt/equity)

## Questions to Ask If Uncertain
1. If the business **fails completely**, does the investor **lose their entire investment**, or is some amount covered by the bank?
2. Is the profit-share **dependent on actual reported profit**, or is it **guaranteed regardless of performance**?
3. Can the investor **walk away and get their money back** on short notice, or are they locked in for the full term?
4. If the bank/sponsor **breaches the guarantee**, what is the investor's recourse?
5. Is the "guarantee" issued by the **bank (strong indicator of loan)** or by a third party (insurance)?
6. Are investor losses from **negligence of the manager covered** by the guarantee, or only "market risk"?
7. Does the contract **classify the guarantee as a loan** (e.g., "contingent liability," "off-balance-sheet borrowing")?

## Shariah Status
- **Verdict (Haram)**: Any capital guarantee by bank/sponsor; contract is loan, not partnership
- **Verdict (Halal)**: No guarantee; investor at full risk (can lose everything); return tied to actual profit
- **Confidence Level**: Very High (unanimous across madhabs; AAOIFI explicit)

## Evidence & Citations
- **AAOIFI Shariah Standard 12**: "Guarantees of capital in Musharaka collapse the partnership into a loan. Capital provider can only be protected by actual profit/loss sharing."
- **Islamic Bankers Center (Malaysia, 2024)**: "Letter of Undertaking (LOU) is widespread in Malaysian Islamic banking; converts Musharaka into debt-like instrument (200-400% capital charge becomes 50-100%). Structurally invalidates partnership."
- **Febianto (2024, Cited 21x)**: "Risk management in Mudharabah/Musharaka: Capital protection mechanisms render the structure a loan. Investors seeking guarantees should accept lower returns (debt-like) or maintain risk exposure (true equity)."
- **IFSB Core Principles**: "Investment accounts with capital guarantees must be reclassified as debt, not equity. Such products are not true Musharaka/Mudaraba."
- **State Bank Pakistan**: "Guarantees in Musharaka invalidate the structure. True partnership requires loss-bearing."
- **Islamic Finance Singapore**: "Guarantee clauses in partnership structures are red flags for Shariah non-compliance."

## SHARAH Engine Use
- **Applicable to**: partnership_like structures; investment products claiming Musharaka/Mudaraba
- **Confidence impact**: If **guarantee present** → -50 (hard fail, converts to loan); if **no guarantee + clear risk-sharing** → +25
- **Trigger keywords**: ["guarantee", "Letter of Undertaking", "LOU", "capital protected", "principal guaranteed", "buyback", "floor return", "exit guarantee"]
- **Sample verdicts**:
  - `IF ("guarantee" OR "capital protected" OR "LOU" OR "buyback option") AND product_type contains "musharaka/mudaraba" THEN issue="Guarantee present; structure is disguised loan, not partnership" principle_tag="riba" confidence_adjust="-50" is_halal=false`

## Post-MVP LLM Use
- LLM **cannot** call a guaranteed product "partnership"
- LLM must flag guarantee as hard fail
