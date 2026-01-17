
import chromadb
from app.core.config import settings
from app.services.embedding import EmbeddingService
import asyncio

async def test_retrieval():
    embedding_service = EmbeddingService()
    query = "What is name of condidate ?"
    
    # Generate embedding
    query_embedding = await embedding_service.get_embedding(query)
    
    # Query Chroma
    client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
    collection = client.get_collection(name="resume_vectors")
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=['documents', 'distances']
    )
    
    print(f"Query: {query}")
    for i, doc in enumerate(results['documents'][0]):
        dist = results['distances'][0][i]
        print(f"--- Result {i} (Distance: {dist}) ---")
        print(doc[:200].replace('\n', ' '))
        print("...")

if __name__ == "__main__":
    asyncio.run(test_retrieval())
