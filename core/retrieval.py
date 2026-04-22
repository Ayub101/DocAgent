import re
from typing import List
from core.chunking import Chunk

_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")

def tokenize(text: str) -> set[str]:
    return set(tok.lower() for tok in _TOKEN_RE.findall(text))

def score_chunk(question: str, chunk_text: str) -> float:
    q_tokens = tokenize(question)
    c_tokens = tokenize(chunk_text)

    if not q_tokens or not c_tokens:
        return 0.0

    overlap = q_tokens & c_tokens
    overlap_score = len(overlap) / len(q_tokens)
    density_score = len(overlap) / max(len(c_tokens), 1)
    phrase_bonus = 0.15 if question.lower() in chunk_text.lower() else 0.0
    heading_bonus = 0.05 if re.search(r"^#{1,6}\s+", chunk_text, flags=re.M) else 0.0

    return overlap_score + density_score * 0.5 + phrase_bonus + heading_bonus

def rank_chunks(question: str, chunks: List[Chunk], top_k: int = 5) -> List[Chunk]:
    for chunk in chunks:
        chunk.score = score_chunk(question, chunk.text)

    ranked = sorted(chunks, key=lambda c: c.score, reverse=True)
    selected = [c for c in ranked if c.score > 0][:top_k]

    if not selected:
        selected = ranked[:top_k]

    return selected

def build_context_block(chunks: List[Chunk]) -> str:
    parts = []
    for c in chunks:
        parts.append(f"[Chunk {c.chunk_id}]\n{c.text}")
    return "\n\n---\n\n".join(parts)