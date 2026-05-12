from app.rag.chunking import ComplaintChunker


def test_chunker_overlaps_long_text() -> None:
    chunker = ComplaintChunker(chunk_size=10, overlap=2)
    chunks = chunker.split("abcdefghijklmnopqrstuvwxyz")

    assert [chunk.index for chunk in chunks] == [0, 1, 2]
    assert chunks[1].text.startswith("ij")

