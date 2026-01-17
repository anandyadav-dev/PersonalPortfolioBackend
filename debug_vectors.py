
import chromadb
from app.core.config import settings

client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
collection = client.get_collection(name="resume_vectors")

print(f"Total documents: {collection.count()}")
results = collection.get()
for i, doc in enumerate(results['documents']):
    print(f"--- Chunk {i} ---")
    print(doc[:200].replace('\n', ' ')) # Print first 200 chars
    print("...")
