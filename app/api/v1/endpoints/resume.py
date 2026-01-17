from fastapi import APIRouter, UploadFile, File, HTTPException, status, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import json
import os
from app.services.pdf_loader import PDFLoaderService
from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService
from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService
from app.services.portfolio_content import PortfolioContentService

router = APIRouter()

# Instantiate services
chunk_service = ChunkingService()
embedding_service = EmbeddingService()
vector_store_service = VectorStoreService()
llm_service = LLMService()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat_resume(request: ChatRequest):
    """
    Answers a question based on stored resume data.
    """
    question = request.question
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # 1. Embed Question
    try:
        query_embedding = await embedding_service.get_embedding(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")

    # 2. Retrieve Context
    try:
        results = vector_store_service.query_similar(query_embedding, n_results=10)
        context_chunks = results.get('documents', [[]])[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

    # 3. Generate Answer
    try:
        answer = await llm_service.generate_answer(question, "\n\n".join(context_chunks))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Answer generation failed: {str(e)}")

    return {
        "question": question,
        "answer": answer,
        "context_used": context_chunks
    }

@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Uploads a resume PDF, extracts text, chunks it, embeds it, and stores it in the vector database.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed."
        )

    # 1. Extract Text
    try:
        text = await PDFLoaderService.extract_text(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    # 2. Chunk Text
    chunks = chunk_service.chunk_text(text)
    
    if not chunks:
        raise HTTPException(status_code=400, detail="Text was too short to chunk.")

    # 3. Generate Embeddings
    try:
        embeddings = await embedding_service.get_embeddings(chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")

    # 4. Store in Vector DB
    try:
        doc_ids = vector_store_service.add_documents(documents=chunks, embeddings=embeddings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector storage failed: {str(e)}")

    return {"message": "Resume uploaded and processed successfully", "chunks_count": len(chunks)}


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    
    # Initialize services
    # Determine base path for portfolio content (Repo Root)
    # Backend is d:\Coding\PersonalPortfolio\backend
    # Repo Root is d:\Coding\PersonalPortfolio
    base_path = r"d:\Coding\PersonalPortfolio"
    portfolio_service = PortfolioContentService(base_path=base_path) 
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            question = payload.get("question")
            use_web_search = payload.get("use_web_search", False)

            if not question:
                await websocket.send_json({"error": "Question not provided"})
                continue

            # Notify start
            await websocket.send_json({"status": "start"})

            # 1. Embed Question
            try:
                query_embedding = await embedding_service.get_embedding(question)
            except Exception as e:
                await websocket.send_json({"error": f"Embedding generation failed: {str(e)}"})
                continue

            # 2. Retrieve Resume Context
            context_text = ""
            try:
                results = vector_store_service.query_similar(query_embedding, n_results=10)
                chunks = results.get('documents', [[]])[0]
                context_text = "\n\n".join(chunks)
            except Exception as e:
                print(f"Retrieval warning: {e}") 
                # Proceed even if retrieval fails

            # 3. (Optional) Retrieve Portfolio Context
            if use_web_search:
                print("Fetching simulated web search content...")
                try:
                    site_content = portfolio_service.get_site_content()
                    context_text += f"\n\n=== LIVE PORTFOLIO WEBSITE CONTENT ===\n{site_content}\n"
                except Exception as e:
                     print(f"Web search error: {e}")

            # 4. Stream Answer
            async for token in llm_service.stream_answer(question, context_text):
                 await websocket.send_json({"token": token})

            await websocket.send_json({"status": "done"})

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_json({"error": str(e)})
            await websocket.close()
        except:
            pass
