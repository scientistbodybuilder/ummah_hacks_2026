"""Knowledge base loader with caching."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import re


@dataclass(frozen=True)
class DocChunk:
    """Represents a knowledge base chunk."""
    id: str
    title: str
    keywords: List[str]
    text: str
    source: str


_KB_CACHE: List[DocChunk] | None = None


def load_kb() -> List[DocChunk]:
    """
    Loads markdown files from data/shariah_kb/ relative to sharah-backend.
    Cached in memory so we don't re-read files every request.
    """
    global _KB_CACHE
    if _KB_CACHE is not None:
        return _KB_CACHE

    # engine/kb_loader.py -> engine -> sharah-backend
    backend_root = Path(__file__).resolve().parent.parent
    kb_dir = backend_root / "data" / "shariah_kb"

    if not kb_dir.exists():
        raise FileNotFoundError(f"KB directory not found at: {kb_dir}")

    chunks: List[DocChunk] = []
    for path in sorted(kb_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        
        # Extract title (first H1 line)
        title = ""
        lines = text.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Extract keywords
        keywords: List[str] = []
        if 'Keywords:' in text:
            kw_part = text.split('Keywords:')[1]
            # Stop at next # (section header) or end
            kw_line = kw_part.split('#')[0].split('\n')[0].strip()
            if kw_line:
                keywords = [kw.strip().lower() for kw in kw_line.split(',') if kw.strip()]
        
        chunks.append(
            DocChunk(
                id=path.stem,
                title=title or path.stem,
                keywords=keywords,
                text=text,
                source=str(path.relative_to(backend_root)),
            )
        )

    _KB_CACHE = chunks
    return chunks


def get_kb() -> List[DocChunk]:
    """Alias for load_kb()."""
    return load_kb()
