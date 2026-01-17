from openai import AsyncOpenAI
from app.core.config import settings
from typing import AsyncGenerator

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o" # Or gpt-3.5-turbo if preferred

    async def generate_answer(self, question: str, context: str) -> str:
        system_prompt = (
            "You are Anand AI's professional AI assistant.\n"
            "Rules:\n"
            "1. Answer ONLY based on the provided Context (Resume/Portfolio).\n"
            "2. EXCEPTION: You may explicitly state your name ('Anand AI') and role if asked directly.\n"
            "3. If the answer is not in the context (and not about your identity), strictly state: 'I am not sure about that, as it is not mentioned in the portfolio.'\n"
            "4. You can respond to normal greetings (Hi, Hello) politely and briefly.\n"
            "5. Do NOT answer general knowledge questions or questions unrelated to Anand."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content

    async def stream_answer(self, question: str, context: str) -> AsyncGenerator[str, None]:
        system_prompt = (
            "You are Anand AI's professional AI assistant.\n"
            "Rules:\n"
            "1. Answer ONLY based on the provided Context (Resume/Portfolio).\n"
            "2. EXCEPTION: You may explicitly state your name ('Anand AI') and role if asked directly.\n"
            "3. If the answer is not in the context (and not about your identity), strictly state: 'I am not sure about that, as it is not mentioned in the portfolio.'\n"
            "4. You can respond to normal greetings (Hi, Hello) politely and briefly.\n"
            "5. Do NOT answer general knowledge questions or questions unrelated to Anand."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            temperature=0.7
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
