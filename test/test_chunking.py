from core.chunking import split_markdown_into_chunks

def test_split_markdown_into_chunks():
    text = "# Title\n\nParagraph one.\n\nParagraph two.\n\nParagraph three."
    chunks = split_markdown_into_chunks(text, max_chars=30)
    assert len(chunks) >= 2
    assert chunks[0].chunk_id == 1
    assert chunks[0].text