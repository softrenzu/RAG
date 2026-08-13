from app.ingestion.chunker import chunk_text


def test_chunk_text_splits_long_input():
    text = "A" * 2200
    chunks = chunk_text(text, chunk_size=900, overlap=150)
    assert len(chunks) >= 3
    assert all(len(chunk) <= 900 for chunk in chunks)


def test_chunk_text_keeps_short_input():
    assert chunk_text("hello", chunk_size=900, overlap=150) == ["hello"]
