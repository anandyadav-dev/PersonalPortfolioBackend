from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import resume
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# CORS Setup
origins = [
    "http://localhost:5173", # Frontend URL
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(resume.router, prefix="/api/v1/resume", tags=["resume"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Resume RAG Chatbot API (OpenAI)"}
