from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    id: str
    source_id: str
    text: str
    position: int


def chunk_text(source_id: str, text: str, size: int = 120, overlap: int = 20) -> list[Chunk]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("overlap must be >= 0 and smaller than size")
    chunks: list[Chunk] = []
    step = size - overlap
    for position, start in enumerate(range(0, len(text), step)):
        piece = text[start:start + size].strip()
        if piece:
            chunks.append(Chunk(f"{source_id}:{position}", source_id, piece, position))
    return chunks
