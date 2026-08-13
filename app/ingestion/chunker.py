def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for paragraph in paragraphs:
        candidate = paragraph if not current else current + "\n\n" + paragraph
        if len(candidate) <= chunk_size:
            current = candidate
            continue
        if current:
            chunks.append(current)
        if len(paragraph) <= chunk_size:
            current = paragraph
            continue
        step = max(1, chunk_size - overlap)
        for start in range(0, len(paragraph), step):
            chunks.append(paragraph[start:start + chunk_size])
        current = ""
    if current:
        chunks.append(current)
    return chunks
