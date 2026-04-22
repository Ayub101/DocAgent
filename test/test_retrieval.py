from core.chunking import Chunk
from core.retrieval import rank_chunks

def test_rank_chunks():
    chunks = [
        Chunk(1, "This page is about apples and oranges."),
        Chunk(2, "This page is about bananas and grapes."),
        Chunk(3, "Unrelated text."),
    ]
    ranked = rank_chunks("What about apples?", chunks, top_k=1)
    assert ranked[0].chunk_id == 1