"""Deterministic rule checks based on extracted facts."""

from __future__ import annotations

from typing import Literal, List
from pydantic import BaseModel
from engine.facts_extractor import ContractFacts, Quote


class Issue(BaseModel):
    """A compliance issue found by rule checks."""
    principle: Literal["riba", "gharar", "maysir", "asset_backing", "late_fees", "guarantee", "other"]
    severity: Literal["low", "medium", "high"]
    explanation: str
    evidence_chunk_ids: List[str] = []
    quotes: List[Quote] = []


def run_rule_checks(facts: ContractFacts, text: str) -> List[Issue]:
    """
    Run deterministic rule checks based on extracted facts.
    Returns list of issues found.
    """
    issues: List[Issue] = []
    
    # Riba check: interest/APR present
    if facts.interest_or_apr_present or facts.interest_rate is not None:
        quotes = [q for q in facts.quotes if q.field == "interest_rate"]
        issues.append(Issue(
            principle="riba",
            severity="high",
            explanation="Interest or APR detected in contract. Riba (usury) is strictly prohibited in Islamic finance.",
            evidence_chunk_ids=["chunk_01_riba_core", "chunk_03_riba_vs_murabaha"],
            quotes=quotes
        ))
    
    # Guarantee + profit sharing check
    if facts.guaranteed_return_present and facts.profit_sharing_present:
        quotes = [q for q in facts.quotes if q.field == "guaranteed_return"]
        issues.append(Issue(
            principle="guarantee",
            severity="high",
            explanation="Guaranteed return combined with profit-sharing violates risk-sharing principles. In partnerships (musharaka/mudaraba), both parties must share risk.",
            evidence_chunk_ids=["chunk_05_profit_sharing_guarantee", "chunk_11_musharaka_vs_mudaraba"],
            quotes=quotes
        ))
    
    # Late fee check
    if facts.late_fee_present:
        quotes = [q for q in facts.quotes if q.field == "late_fee"]
        issues.append(Issue(
            principle="late_fees",
            severity="medium",
            explanation="Late fees or penalties detected. These must be handled as ta'widh (compensation) or donated to charity, not retained as profit. Requires scholar review.",
            evidence_chunk_ids=["chunk_04_late_fees_ta_widh", "chunk_07_bnpl_late_fees_gharar"],
            quotes=quotes
        ))
    
    # Gharar check: ambiguity flags
    if facts.ambiguity_flags:
        issues.append(Issue(
            principle="gharar",
            severity="medium",
            explanation=f"Uncertainty or vague terms detected: {', '.join(facts.ambiguity_flags[:3])}. Gharar (excessive uncertainty) is prohibited. Terms must be clear and fixed.",
            evidence_chunk_ids=["chunk_02_gharar_uncertainty", "chunk_10_gharar_vague_terms"],
            quotes=[]
        ))
    
    # Asset backing check for murabaha
    if facts.contract_type_guess == "murabaha":
        if facts.asset_backing_present is False:
            issues.append(Issue(
                principle="asset_backing",
                severity="high",
                explanation="Murabaha (cost-plus sale) requires clear asset backing. The financier must own the asset before selling it. Asset details are unclear or missing.",
                evidence_chunk_ids=["chunk_08_murabaha_asset_backing", "chunk_03_riba_vs_murabaha"],
                quotes=[]
            ))
        elif facts.asset_backing_present is None:
            issues.append(Issue(
                principle="asset_backing",
                severity="medium",
                explanation="Murabaha contract detected but asset backing is unclear. What is the underlying asset and when does ownership transfer?",
                evidence_chunk_ids=["chunk_08_murabaha_asset_backing"],
                quotes=[]
            ))
    
    # General asset backing for sale-like contracts
    if facts.repayment_structure == "cost_plus_sale" and facts.asset_backing_present is False:
        issues.append(Issue(
            principle="asset_backing",
            severity="medium",
            explanation="Cost-plus sale structure detected but underlying asset is not clearly identified.",
            evidence_chunk_ids=["chunk_08_murabaha_asset_backing"],
            quotes=[]
        ))
    
    return issues
