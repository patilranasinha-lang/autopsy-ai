from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from ai_engine.investigator.llm_orchestrator import LLMOrchestrator
from ai_engine.investigator.conversation_memory import ConversationMemory

router = APIRouter()
orchestrator = LLMOrchestrator()
memory = ConversationMemory()

class ChatRequest(BaseModel):
    user_id: int
    query: str

class BackgroundIndexRequest(BaseModel):
    user_id: int
    raw_data_points: list

@router.post("/message")
async def chat_message(request: ChatRequest):
    try:
        # Process RAG query
        result = orchestrator.process_query(request.user_id, request.query)
        
        # Save to memory
        memory.append_interaction(request.user_id, request.query, result["response"])
        
        return {
            "status": "success",
            "reply": result["response"],
            "evidence": result["evidence_used"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{user_id}")
async def get_history(user_id: int):
    return {"history": memory.get_history(user_id)}

@router.post("/index")
async def index_data(request: BackgroundIndexRequest, background_tasks: BackgroundTasks):
    # In a real app, this would trigger ai_engine/rag/document_chunker.py and vector_store.py
    # inside a background task to prevent blocking HTTP response.
    return {"status": "indexing_started"}
