from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    text: str
    index: int


class ComplaintChunker:
    def __init__(self, chunk_size: int, overlap: int) -> None:
        if overlap >= chunk_size:
            raise ValueError("chunk overlap must be smaller than chunk size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> list[TextChunk]:
        if len(text) <= self.chunk_size:
            return [TextChunk(text=text, index=0)]

        chunks: list[TextChunk] = []
        start = 0
        index = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(TextChunk(text=text[start:end], index=index))
            if end == len(text):
                break
            start = end - self.overlap
            index += 1
        return chunks

