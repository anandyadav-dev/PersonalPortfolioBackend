from openai import AsyncOpenAI
from app.core.config import settings
from typing import List

class EmbeddingService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"

    async def get_embedding(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        response = await self.client.embeddings.create(input=[text], model=self.model)
        return response.data[0].embedding

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        # OpenAI supports batching
        response = await self.client.embeddings.create(input=texts, model=self.model)
        # Sort by index to ensure order if necessary (OpenAI usually preserves order)
        return [data.embedding for data in response.data]
