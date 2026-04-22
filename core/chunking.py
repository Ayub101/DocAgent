from dataclasses import dataclass
from typing import List
import re

from utils.text import normalize_whitespace

@dataclass
class Chunk:
    chunk_id: int
    text: str
    score: float = 0.0

def split_markdown_into_chunks(markdown: str, max_chars: int = 1800, overlap: int = 200) -> List[Chunk]:
    markdown = normalize_whitespace(markdown)
    if not markdown:
        return []

    paragraphs = [p.strip() for p in re.split(r"\n{2,}", markdown) if p.strip()]
    chunks: List[Chunk] = []
    buffer = ""
    chunk_id = 1

    def flush(buf: str):
        nonlocal chunk_id
        if buf.strip():
            chunks.append(Chunk(chunk_id=chunk_id, text=buf.strip()))
            chunk_id += 1

    for para in paragraphs:
        if len(buffer) + len(para) + 2 <= max_chars:
            buffer = f"{buffer}\n\n{para}" if buffer else para
        else:
            flush(buffer)
            if len(para) > max_chars:
                start = 0
                while start < len(para):
                    part = para[start : start + max_chars]
                    chunks.append(Chunk(chunk_id=chunk_id, text=part.strip()))
                    chunk_id += 1
                    start += max(1, max_chars - overlap)
                buffer = ""
            else:
                buffer = para

    flush(buffer)
    return chunks