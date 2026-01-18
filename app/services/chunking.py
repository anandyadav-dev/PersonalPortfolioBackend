from typing import List
import tiktoken
class ChunkingService:
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        # Simple character based chunking for now, or word based
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks
