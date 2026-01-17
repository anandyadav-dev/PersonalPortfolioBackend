import chromadb
from app.core.config import settings
from typing import List, Dict

class VectorStoreService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection(name="resume_chunks")

    def add_documents(self, documents: List[str], embeddings: List[List[float]]) -> List[str]:
        # Simple ID generation
        ids = [str(i) for i in range(len(documents))] 
        # Ideally satisfy uniqueness in meaningful way or use uuid
        import uuid
        ids = [str(uuid.uuid4()) for _ in documents]
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )
        return ids

    def query_similar(self, query_embedding: List[float], n_results: int = 5) -> Dict:
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
