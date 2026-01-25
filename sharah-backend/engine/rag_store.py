# engine/rag_store.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class DocChunk:
    id: str
    source: str
    text: str


_KB_CACHE: List[DocChunk] | None = None


def load_kb() -> List[DocChunk]:
    """
    Loads markdown files from data/shariah_kb/ relative to sharah-backend.
    Cached in memory so we don't re-read files every request.
    """
    global _KB_CACHE
    if _KB_CACHE is not None:
        return _KB_CACHE

    # engine/rag_store.py -> engine -> sharah-backend
    backend_root = Path(__file__).resolve().parent.parent
    kb_dir = backend_root / "data" / "shariah_kb"

    if not kb_dir.exists():
        raise FileNotFoundError(f"KB directory not found at: {kb_dir}")

    chunks: List[DocChunk] = []
    for path in sorted(kb_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        chunks.append(
            DocChunk(
                id=path.stem,
                source=str(path.relative_to(backend_root)),
                text=text,
            )
        )

    _KB_CACHE = chunks
    return chunks
