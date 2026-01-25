"""Orchestrator for unified contract analysis pipeline."""

from __future__ import annotations

import json
from typing import Dict
from engine.pdf_parser import parse_pdf_text
from engine.facts_extractor import extract_contract_facts
from engine.kb_loader import load_kb
from engine.retrieval import retrieve_chunks
from engine.rules import run_rule_checks
from engine.scholar_llm import scholar_ruling
from openai_config import client, model


# Constants
MAX_TEXT_FOR_RETRIEVAL = 2000
MAX_TEXT_FOR_LLM = 20000
TOP_K_CHUNKS = 6


async def analyze_contract_pdf(file_bytes: bytes, filename: str) -> Dict:
    """
    Unified pipeline for contract analysis.
    
    Pipeline:
    1. Parse PDF text
    2. Extract structured facts
    3. Load knowledge base
    4. Retrieve relevant evidence chunks
    5. Run deterministic rule checks
    6. Generate scholar ruling (with or without OpenAI)
    7. Assemble final response
    
    Args:
        file_bytes: PDF file bytes
        filename: Original filename
        
    Returns:
        Complete analysis response dict
    """
    # Step 1: Parse PDF
    try:
        text = parse_pdf_text(file_bytes)
    except ValueError as e:
        raise ValueError(f"PDF parsing failed: {str(e)}")
    
    text_length = len(text)
    text_truncated = text_length > MAX_TEXT_FOR_LLM
    
    # Step 2: Extract facts
    facts = await extract_contract_facts(text)
    
    # Step 3: Load KB
    kb = load_kb()
    
    # Step 4: Build retrieval query
    facts_summary = {
        "contract_type": facts.contract_type_guess,
        "repayment": facts.repayment_structure,
        "interest": facts.interest_or_apr_present,
        "late_fee": facts.late_fee_present,
        "guarantee": facts.guaranteed_return_present,
    }
    retrieval_query = f"{filename}\n{text[:MAX_TEXT_FOR_RETRIEVAL]}\n{json.dumps(facts_summary)}"
    
    # Step 5: Retrieve evidence chunks
    evidence_chunks = retrieve_chunks(retrieval_query, kb, k=TOP_K_CHUNKS)
    
    # Step 6: Run rule checks
    issues = run_rule_checks(facts, text)
    
    # Step 7: Generate scholar ruling
    llm_result = await scholar_ruling(text, facts, issues, evidence_chunks)
    
    # Step 8: Assemble final response
    return {
        "success": True,
        "filename": filename,
        "text_length": text_length,
        "verdict": llm_result["verdict"],
        "confidence": llm_result["confidence"],
        "contract_type": llm_result["contract_type"],
        "summary": llm_result["summary"],
        "reasoning": llm_result["reasoning"],
        "issues": llm_result["issues"],
        "missing_info_questions": llm_result["missing_info_questions"],
        "evidence_used": [
            {
                "chunk_id": ch["chunk_id"],
                "title": ch["title"],
                "score": ch["score"],
                "matched_keywords": ch["matched_keywords"]
            }
            for ch in evidence_chunks
        ],
        "extracted_facts": facts.model_dump(),
        "_metadata": {
            "chunks_considered": len(kb),
            "chunks_returned": len(evidence_chunks),
            "openai_configured": client is not None and model is not None,
            "model_used": model if (client is not None and model is not None) else None,
            "llm_error": llm_result.get("_llm_error"),
            "text_truncated": text_truncated
        }
    }
