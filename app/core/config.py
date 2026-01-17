import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Resume RAG Chatbot"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    CHROMA_DB_DIR: str = os.path.join(os.getcwd(), "chroma_db")

settings = Settings()
