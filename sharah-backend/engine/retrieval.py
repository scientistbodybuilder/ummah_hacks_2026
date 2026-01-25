"""Hybrid retrieval with keyword and token overlap scoring."""

from __future__ import annotations

import re
from typing import List, Dict
from engine.kb_loader import DocChunk


def retrieve_chunks(query_text: str, chunks: List[DocChunk], k: int = 6) -> List[Dict]:
    """
    Returns top-k chunks by hybrid scoring:
    - Token overlap between query and chunk text
    - Keyword hits (weighted 2x)
    
    Args:
        query_text: Text to match against
        chunks: List of DocChunk to search
        k: Number of chunks to return
        
    Returns:
        List of dicts with chunk_id, title, score, matched_keywords, source, excerpt
    """
    query_lower = query_text.lower()
    query_tokens = set(re.findall(r"[a-z]+", query_lower))
    
    scored: List[tuple[float, DocChunk, List[str]]] = []
    
    for chunk in chunks:
        # Token overlap score
        chunk_tokens = set(re.findall(r"[a-z]+", chunk.text.lower()))
        overlap_score = len(query_tokens.intersection(chunk_tokens))
        
        # Keyword hit count (weighted 2x)
        matched_keywords: List[str] = []
        for keyword in chunk.keywords:
            # Simple "in" check on normalized text
            if keyword in query_lower:
                matched_keywords.append(keyword)
        
        keyword_hit_count = len(matched_keywords)
        
        # Hybrid score
        score = overlap_score + 2 * keyword_hit_count
        
        if score > 0:
            scored.append((score, chunk, matched_keywords))
    
    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Return top-k as dicts
    results: List[Dict] = []
    seen_ids = set()
    
    for score, chunk, matched_keywords in scored[:k]:
        # Avoid duplicates
        if chunk.id in seen_ids:
            continue
        seen_ids.add(chunk.id)
        
        # Get excerpt (first ~400 chars)
        excerpt = chunk.text[:400] + "..." if len(chunk.text) > 400 else chunk.text
        
        results.append({
            "chunk_id": chunk.id,
            "title": chunk.title,
            "score": float(score),
            "matched_keywords": matched_keywords,
            "source": chunk.source,
            "excerpt": excerpt,
            "full_text": chunk.text,  # Keep available for LLM
        })
    
    return results
