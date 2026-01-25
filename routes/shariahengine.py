# routes/shariah_engine.py
from __future__ import annotations

from services.rag_store import load_kb
from services.retriever import retrieve
from services.llm_reasoner import (
    build_missing_info_questions,
    build_reasoning_with_evidence,
    build_recommendation_with_questions,
)





from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional
import re

from pydantic import BaseModel, Field


# -------------------------
# Schemas (keep here for hackathon simplicity)
# -------------------------

class ShariaCheckRequest(BaseModel):
    product_type: str = Field(..., min_length=1, max_length=50)
    interest_rate: float = Field(..., ge=0, le=50)         # % annual
    profit_sharing_pct: float = Field(..., ge=0, le=100)   # allow >50 for edge cases
    terms_length_months: int = Field(..., ge=1, le=120)
    description: str = Field(..., min_length=5, max_length=5000)


class ShariaCheckResponse(BaseModel):
    is_shariah_compliant: bool
    confidence: float
    reasoning: str
    flagged_issues: List[str]
    applicable_fatwas: List[str]
    recommendation: str
    evidence_used: List[str] = []



# -------------------------
# Internal structures
# -------------------------

@dataclass
class ExtractedFeatures:
    has_interest_words: bool
    has_profit_share_words: bool
    has_fixed_repayment_words: bool
    has_late_fee_words: bool
    has_compounding_words: bool
    has_asset_words: bool
    has_uncertainty_words: bool
    has_guarantee_words: bool
    has_buyback_words: bool
    mentions_markup_words: bool


# -------------------------
# Keyword sets (hackathon friendly)
# -------------------------

KW_INTEREST = {"interest", "apr", "rate", "percent interest", "coupon"}
KW_PROFIT_SHARE = {"profit share", "revenue share", "musharaka", "mudaraba", "partnership", "profit-sharing"}
KW_FIXED_REPAY = {"fixed repayment", "fixed payback", "repay", "repayment", "installment", "emi", "principal"}
KW_LATE_FEE = {"late fee", "penalty", "default fee", "missed payment fee"}
KW_COMPOUND = {"compound", "compounding"}
KW_ASSET = {"asset", "inventory", "equipment", "car", "house", "property", "commodity", "gold", "purchase", "sale", "murabaha"}
KW_UNCERTAIN = {"to be determined", "tbd", "may change", "variable at our discretion", "subject to approval"}
KW_GUARANTEE = {"guarantee", "guaranteed return", "capital protected", "principal protected"}
KW_BUYBACK = {"buyback", "repurchase", "purchase option"}
KW_MARKUP = {"markup", "cost-plus", "murabaha"}


def _contains_any(text: str, keywords: set[str]) -> bool:
    t = text.lower()
    return any(k in t for k in keywords)


def extract_features(description: str) -> ExtractedFeatures:
    return ExtractedFeatures(
        has_interest_words=_contains_any(description, KW_INTEREST),
        has_profit_share_words=_contains_any(description, KW_PROFIT_SHARE),
        has_fixed_repayment_words=_contains_any(description, KW_FIXED_REPAY),
        has_late_fee_words=_contains_any(description, KW_LATE_FEE),
        has_compounding_words=_contains_any(description, KW_COMPOUND),
        has_asset_words=_contains_any(description, KW_ASSET),
        has_uncertainty_words=_contains_any(description, KW_UNCERTAIN),
        has_guarantee_words=_contains_any(description, KW_GUARANTEE),
        has_buyback_words=_contains_any(description, KW_BUYBACK),
        mentions_markup_words=_contains_any(description, KW_MARKUP),
    )


def classify_contract(req: ShariaCheckRequest, f: ExtractedFeatures) -> str:
    """
    Returns one of: loan_like, partnership_like, sale_like, unclear
    Hackathon heuristic:
    - If interest_rate > 0 OR mentions interest words + fixed repayment -> loan_like
    - If profit_sharing_pct > 0 OR mentions partnership words -> partnership_like
    - If mentions markup/asset/purchase/sale -> sale_like
    - else unclear
    """
    # strong loan signals
    if req.interest_rate > 0:
        return "loan_like"
    if f.has_interest_words and f.has_fixed_repayment_words:
        return "loan_like"
    if f.has_compounding_words:
        return "loan_like"

    # strong partnership signals
    if req.profit_sharing_pct > 0 or f.has_profit_share_words:
        return "partnership_like"

    # sale signals
    if f.has_asset_words or f.mentions_markup_words or req.product_type.lower() == "murabahah":
        return "sale_like"

    return "unclear"


def run_checks(req: ShariaCheckRequest, f: ExtractedFeatures, contract: str) -> Tuple[bool, List[str], List[str]]:
    """
    Returns: (is_compliant_guess, flagged_issues, fatwas)
    """
    issues: List[str] = []
    fatwas: List[str] = []

    # RIBA checks (hard fail when loan-like + interest)
    if contract == "loan_like":
        if req.interest_rate > 0 or f.has_interest_words or f.has_compounding_words:
            issues.append("Riba risk: loan-like structure with interest/return on money.")
            fatwas.append("riba")

    # Late fee check (usually needs scholar review; treat as issue)
    if f.has_late_fee_words:
        issues.append("Late fee/penalty mentioned: ensure penalties are not profit (often donated).")
        fatwas.append("late-fees")

    # Gharar check (unclear terms)
    if f.has_uncertainty_words:
        issues.append("Gharar risk: uncertain/vague terms detected.")
        fatwas.append("gharar")

    # Partnership checks
    if contract == "partnership_like":
        fatwas.append("musharaka/mudaraba")
        fatwas.append("profit-sharing")
        if f.has_guarantee_words:
            issues.append("Guarantee mentioned: guaranteed return/capital can violate partnership risk-sharing.")
            fatwas.append("risk-sharing")

    # Sale checks (Murabaha-ish)
    if contract == "sale_like":
        fatwas.append("murabaha/sale")
        if not f.has_asset_words:
            issues.append("Sale-like product but asset details unclear: what is bought/sold and when ownership transfers?")
            fatwas.append("asset-backing")

    # Basic input logic sanity checks
    if req.interest_rate == 0 and req.profit_sharing_pct == 0 and contract == "unclear":
        issues.append("Insufficient structure info: cannot classify contract confidently.")
        fatwas.append("needs-more-info")

    # compliance guess:
    # - If riba issue exists -> noncompliant guess
    # - otherwise compliant guess (but may be medium confidence)
    is_compliant_guess = True
    if any("Riba risk" in x for x in issues):
        is_compliant_guess = False

    # de-dup fatwas
    fatwas = sorted(list(set(fatwas)))
    return is_compliant_guess, issues, fatwas


def score_confidence(req: ShariaCheckRequest, contract: str, issues: List[str]) -> float:
    """
    Confidence should reflect:
    - completeness (can we classify?)
    - severity (hard fails)
    - ambiguity (gharar/late fee => reduces confidence)
    """
    base = 65.0

    # classification strength
    if contract == "unclear":
        base -= 20
    else:
        base += 5

    # hard fail increases confidence in "not compliant"
    if any("Riba risk" in x for x in issues):
        base += 15  # we're confident it's problematic

    # ambiguity reducers
    if any("Gharar risk" in x for x in issues):
        base -= 15
    if any("Late fee/penalty" in x for x in issues):
        base -= 10
    if any("asset details unclear" in x.lower() for x in issues):
        base -= 10
    if any("cannot classify" in x.lower() for x in issues):
        base -= 20

    # small boost for strong “clean” cases
    if (req.interest_rate == 0) and (req.profit_sharing_pct > 0) and contract == "partnership_like" and len(issues) == 0:
        base += 10

    # clamp
    return float(max(0, min(100, round(base, 1))))


def generate_reasoning(
    req: ShariaCheckRequest,
    contract: str,
    is_compliant: bool,
    issues: List[str],
    fatwas: List[str],
    confidence: float,
) -> str:
    parts: List[str] = []
    parts.append(f"Classified structure as **{contract.replace('_', ' ')}** based on provided fields and description.")
    parts.append(f"Interest rate: {req.interest_rate}%, Profit-sharing: {req.profit_sharing_pct}%.")

    if is_compliant:
        parts.append("No clear riba (interest-on-loan) violation detected from the available information.")
    else:
        parts.append("Detected a **riba risk** because the product looks loan-like with interest/return on money.")

    if issues:
        parts.append("Flagged issues:")
        for i in issues:
            parts.append(f"- {i}")

    if fatwas:
        parts.append("Applicable principles:")
        parts.append(", ".join(fatwas))

    parts.append(f"Confidence reflects contract clarity + severity of issues: **{confidence}%**.")
    return "\n".join(parts)


def generate_recommendation(is_compliant: bool, issues: List[str], contract: str) -> str:
    if not is_compliant:
        return "Not compliant as described. Remove interest-on-loan mechanics or restructure as sale/partnership with proper risk-sharing."
    if any("Gharar risk" in x for x in issues) or any("Late fee/penalty" in x for x in issues):
        return "Likely compliant, but recommend Shariah scholar review of flagged clauses (especially penalties/uncertain terms)."
    if contract == "unclear":
        return "Provide more structural details (who owns what, repayment mechanics, penalties) to classify contract confidently."
    return "Compliant based on provided information. Prepare for Shariah board review with the listed audit trail."


async def check_shariah_compliance(request: ShariaCheckRequest) -> ShariaCheckResponse:
    # 1) Deterministic engine (your original pipeline)
    f = extract_features(request.description)
    contract = classify_contract(request, f)
    is_compliant_guess, issues, fatwas = run_checks(request, f, contract)
    confidence = score_confidence(request, contract, issues)

    base_reasoning = generate_reasoning(
        request, contract, is_compliant_guess, issues, fatwas, confidence
    )
    base_recommendation = generate_recommendation(is_compliant_guess, issues, contract)

    # 2) RAG: retrieve evidence chunks relevant to this product
    kb = load_kb()
    query = f"{request.product_type}\n{request.description}"
    evidence = retrieve(query, kb, k=4)
    evidence_ids = [ch.id for ch in evidence]

    # 3) “Reasoner” (deterministic for now): add citations + missing-info questions
    questions = build_missing_info_questions(issues, contract)
    reasoning = build_reasoning_with_evidence(base_reasoning, evidence)
    recommendation = build_recommendation_with_questions(base_recommendation, questions)

    # 4) Return response
    return ShariaCheckResponse(
        is_shariah_compliant=is_compliant_guess,
        confidence=confidence,
        reasoning=reasoning,
        flagged_issues=issues,
        applicable_fatwas=fatwas,
        recommendation=recommendation,
        evidence_used=evidence_ids,
    )

