# engine/llm_reasoner.py
from __future__ import annotations

from typing import List
from engine.rag_store import DocChunk


def build_missing_info_questions(flagged_issues: List[str], contract: str) -> List[str]:
    qs: List[str] = []

    # Questions triggered by issues
    if any("late fee" in x.lower() for x in flagged_issues):
        qs.append("If there are penalties/late fees, are they donated (not retained as profit)?")

    if any("uncertain" in x.lower() or "gharar" in x.lower() for x in flagged_issues):
        qs.append("Which terms are fixed vs variable (pricing, penalties, repayment mechanics), and who can change them?")

    if any("asset" in x.lower() for x in flagged_issues):
        qs.append("What is the underlying asset, and when does ownership transfer?")

    if any("guarantee" in x.lower() for x in flagged_issues):
        qs.append("Is any return or capital guaranteed regardless of outcome? If yes, how is that structured?")

    # If contract is unclear, ask clarifiers
    if contract == "unclear":
        qs.append("Is this primarily a loan, a sale (cost-plus), a lease, or a partnership? Describe cashflows and obligations.")

    # de-dup while preserving order
    out = []
    seen = set()
    for q in qs:
        if q not in seen:
            out.append(q)
            seen.add(q)
    return out


def build_reasoning_with_evidence(base_reasoning: str, evidence: List[DocChunk]) -> str:
    if not evidence:
        return base_reasoning + "\n\nEvidence: (none retrieved)"

    ids = ", ".join([ch.id for ch in evidence])
    return base_reasoning + f"\n\nEvidence chunks used: {ids}"


def build_recommendation_with_questions(base_recommendation: str, questions: List[str]) -> str:
    if not questions:
        return base_recommendation
    qtext = "\n".join([f"- {q}" for q in questions])
    return base_recommendation + "\n\nTo increase confidence, answer:\n" + qtext
