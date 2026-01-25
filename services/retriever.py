# services/retriever.py
from __future__ import annotations

import re
from typing import List, Tuple
from services.rag_store import DocChunk


def _tokenize(text: str) -> set[str]:
    # simple word tokens; hackathon-friendly
    return set(re.findall(r"[a-zA-Z]+", text.lower()))


def retrieve(query: str, chunks: List[DocChunk], k: int = 4) -> List[DocChunk]:
    """
    Returns top-k chunks by keyword overlap with query.
    Think: “search most relevant docs” without embeddings.
    """
    q = _tokenize(query)

    scored: List[Tuple[int, DocChunk]] = []
    for ch in chunks:
        t = _tokenize(ch.text)
        score = len(q.intersection(t))
        scored.append((score, ch))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [ch for score, ch in scored[:k] if score > 0]
