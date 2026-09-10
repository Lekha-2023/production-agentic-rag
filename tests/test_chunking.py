from app.chunking import chunk_text


def test_chunking_creates_overlap():
    chunks = chunk_text("doc", "abcdefghijklmnopqrstuvwxyz", size=10, overlap=2)
    assert len(chunks) >= 3
    assert chunks[0].text[-2:] == chunks[1].text[:2]
    assert chunks[0].source_id == "doc"
