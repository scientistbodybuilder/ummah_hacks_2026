"""LLM-powered scholar ruling generation."""

from __future__ import annotations

import json
from typing import Dict, List
from openai_config import client, model
from engine.facts_extractor import ContractFacts
from engine.rules import Issue


async def scholar_ruling(
    text: str,
    facts: ContractFacts,
    issues: List[Issue],
    evidence_chunks: List[Dict]
) -> Dict:
    """
    Generate a Shariah scholar-style ruling using OpenAI.
    Falls back to deterministic response if OpenAI not configured.
    """
    if client is None or model is None:
        return _fallback_ruling(facts, issues)
    
    # Build prompt
    system_prompt = """You are a Shariah compliance reviewer. Analyze the contract based ONLY on facts present in the text or provided evidence.
If something is unknown or unclear, explicitly state "unknown" or "unclear" and ask questions.
Do not invent details that are not in the text.
Cite specific evidence chunk IDs when referencing Shariah principles.
Provide a scholar-style ruling with clear verdict and reasoning."""

    # Format evidence chunks
    evidence_text = ""
    for i, chunk in enumerate(evidence_chunks, 1):
        evidence_text += f"\n=== Evidence {i}: {chunk['title']} (ID: {chunk['chunk_id']}) ===\n"
        evidence_text += chunk['full_text'][:2000]  # Limit each chunk
        evidence_text += "\n"
    
    # Format issues
    issues_json = [issue.model_dump() for issue in issues]
    
    # Truncate text if too long
    text_truncated = len(text) > 20000
    text_for_prompt = text[:20000]
    if text_truncated:
        text_for_prompt += "\n\n[Text truncated for length]"
    
    user_prompt = f"""Analyze this contract for Shariah compliance:

--- EXTRACTED FACTS ---
{json.dumps(facts.model_dump(), indent=2)}

--- DETERMINISTIC ISSUES FOUND ---
{json.dumps(issues_json, indent=2)}

--- RELEVANT SHARIAH EVIDENCE ---
{evidence_text}

--- CONTRACT TEXT (first 20k chars) ---
{text_for_prompt}

Provide your ruling in JSON format:
{{
  "verdict": "compliant" | "non-compliant" | "uncertain",
  "confidence": 0-100,
  "contract_type": "{facts.contract_type_guess}",
  "summary": "<brief summary>",
  "reasoning": "<detailed scholar-style reasoning with citations to evidence chunk IDs>",
  "issues": [
    {{
      "principle": "riba|gharar|maysir|asset_backing|late_fees|guarantee|other",
      "severity": "low|medium|high",
      "description": "<description>",
      "evidence_chunk_ids": ["chunk_01_riba_core", ...],
      "quotes": [{{"field": "...", "quote": "..."}}]
    }}
  ],
  "missing_info_questions": ["<question>"],
  "evidence_used": ["chunk_01_riba_core", ...]
}}

Ensure you cite evidence chunk IDs in your reasoning when referencing Shariah principles."""

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        
        # Ensure required fields
        result.setdefault("verdict", "uncertain")
        result.setdefault("confidence", 50)
        result.setdefault("contract_type", facts.contract_type_guess)
        result.setdefault("summary", "Analysis completed")
        result.setdefault("reasoning", "")
        result.setdefault("issues", issues_json)
        result.setdefault("missing_info_questions", facts.missing_info_questions)
        result.setdefault("evidence_used", [ch['chunk_id'] for ch in evidence_chunks])
        
        result["_llm_error"] = None
        return result
        
    except Exception as e:
        # Return fallback with error metadata
        fallback = _fallback_ruling(facts, issues)
        fallback["_llm_error"] = str(e)
        return fallback


def _fallback_ruling(facts: ContractFacts, issues: List[Issue]) -> Dict:
    """Generate deterministic ruling when OpenAI not available."""
    # Determine verdict from issues
    high_severity_issues = [i for i in issues if i.severity == "high"]
    if high_severity_issues:
        verdict = "non-compliant"
        confidence = 70
    elif issues:
        verdict = "uncertain"
        confidence = 50
    else:
        verdict = "uncertain"  # Without LLM, can't be fully confident
        confidence = 50
    
    # Build summary
    if high_severity_issues:
        summary = f"Detected {len(high_severity_issues)} high-severity compliance issues. OpenAI analysis not available for detailed review."
    elif issues:
        summary = f"Detected {len(issues)} compliance concerns. OpenAI analysis not available for detailed review."
    else:
        summary = "No obvious compliance issues detected via rule checks. OpenAI analysis not available for comprehensive review."
    
    # Build reasoning
    reasoning_parts = [
        "Analysis performed using deterministic rule checks. OpenAI scholar review not available.",
        f"Contract type: {facts.contract_type_guess}",
        f"Repayment structure: {facts.repayment_structure}",
    ]
    
    if facts.interest_or_apr_present:
        reasoning_parts.append(f"Interest/APR detected: {facts.interest_rate}%")
    if facts.late_fee_present:
        reasoning_parts.append("Late fees detected - requires review for ta'widh/charity handling")
    if facts.guaranteed_return_present:
        reasoning_parts.append("Guaranteed return detected - may violate risk-sharing")
    
    reasoning = "\n".join(reasoning_parts)
    
    # Convert issues to dict format
    issues_dict = [issue.model_dump() for issue in issues]
    
    return {
        "verdict": verdict,
        "confidence": confidence,
        "contract_type": facts.contract_type_guess,
        "summary": summary,
        "reasoning": reasoning,
        "issues": issues_dict,
        "missing_info_questions": facts.missing_info_questions,
        "evidence_used": [],
        "_llm_error": "OpenAI not configured"
    }
