import os
import shutil
import uuid
import asyncio
import re
import time
from typing import List, Optional, Literal

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from factory.rag_factory import RAGPipeline
from services.logger import log
import re

router = APIRouter()

# Base directory for temp files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# Constants and globals
PIPELINE_TTL = 1800  # seconds = 30 minutes
DEFAULT_INGEST_PATHS = [os.path.join(TEMP_DIR, f) for f in os.listdir(TEMP_DIR) if f.endswith(".pdf")]

# Global pipeline instance
global_pipeline = None  # Shared pipeline for all conversations
last_init_time = 0      # Timestamp of last pipeline initialization
pipeline_lock = asyncio.Lock()

# Pydantic models
class Message(BaseModel):
    role: Literal["user", "bot"]
    content: str

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str
    source_docs: Optional[List[dict]] = None

class IngestPathsRequest(BaseModel):
    file_paths: List[str]


def clean_response(text: str) -> str:
    # Remove all references that look like [anypath.pdf:start-end]
    cleaned = re.sub(r"\[.*?\.pdf:\d+-\d+\]", "", text)
    # Optionally remove any empty brackets or remaining square bracketed paths
    cleaned = re.sub(r"\[.*?\.pdf.*?\]", "", cleaned)
    return cleaned.strip()
async def initialize_global_pipeline():
    """Initialize the global pipeline at application startup or when needed"""
    global global_pipeline, last_init_time
    
    if global_pipeline is None or time.time() - last_init_time > 3600:  # Re-init every hour
        if not DEFAULT_INGEST_PATHS:
            log.warning("No default documents found for ingestion")
            return
        
        try:
            log.info("Initializing global pipeline...")
            pipeline = RAGPipeline(DEFAULT_INGEST_PATHS)
            pipeline.ingest()  # Synchronous ingestion
            log.info("Global pipeline initialized and ingested successfully")
            global_pipeline = pipeline
            last_init_time = time.time()
        except Exception as e:
            log.error(f"Failed to initialize global pipeline: {str(e)}")
            raise RuntimeError(f"Global pipeline initialization failed: {str(e)}")

async def save_upload_files(files: List[UploadFile]) -> List[str]:
    saved_paths = []
    for file in files:
        filename = file.filename
        dest_path = os.path.join(TEMP_DIR, filename)
        if os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{uuid.uuid4().hex}{ext}"
            dest_path = os.path.join(TEMP_DIR, filename)
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file.file.close()
        if not os.path.exists(dest_path):
            log.error(f"Failed to save file: {dest_path}")
            raise HTTPException(status_code=500, detail=f"Failed to save file {filename}")
        log.info(f"Saved uploaded file to: {dest_path}")
        saved_paths.append(dest_path)
    return saved_paths

# Initialize global pipeline at startup
if DEFAULT_INGEST_PATHS:
    asyncio.create_task(initialize_global_pipeline())

# Endpoints
@router.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    saved_paths = await save_upload_files(files)
    log.info("Files uploaded", files=saved_paths)
    return {"saved_files": saved_paths}

@router.post("/ingest")
async def ingest_uploaded(files: List[UploadFile] = File(...)):
    """Create a custom pipeline for specific documents"""
    try:
        saved_paths = await save_upload_files(files)
        if not saved_paths:
            raise HTTPException(400, detail="No files uploaded for ingestion.")
        
        # Create a temporary pipeline just for ingestion
        pipeline = RAGPipeline(saved_paths)
        pipeline.ingest()  # Synchronous ingestion
            
        log.info("Ingestion completed successfully", files=saved_paths)
        return {
            "status": "ingested",
            "files": saved_paths
        }

    except Exception as e:
        log.error("Ingestion error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    conversation_id = request.conversation_id or str(uuid.uuid4())
    log.info(f"Received chat request for conversation_id={conversation_id}")

    if not request.messages:
        log.warning(f"No messages provided in chat request for conversation_id={conversation_id}")
        raise HTTPException(status_code=400, detail="No messages provided in the chat request.")

    try:
        # Ensure global pipeline is ready
        if global_pipeline is None:
            await initialize_global_pipeline()
            
            if global_pipeline is None:
                log.error("Global pipeline not available after initialization")
                raise HTTPException(500, detail="Global pipeline not initialized")

        # Build full conversation prompt
        full_prompt = ""
        for msg in request.messages:
            role = "assistant" if msg.role == "bot" else msg.role
            full_prompt += f"{role.capitalize()}: {msg.content}\n"
        log.debug(f"Constructed full prompt for conversation_id={conversation_id}: {full_prompt}")

        # Query the global pipeline
        log.info(f"Querying pipeline for conversation_id={conversation_id}")
        answer_obj, docs = global_pipeline.query(full_prompt)
        log.info(f"Received response from pipeline for conversation_id={conversation_id}")

        if hasattr(answer_obj, "message") and hasattr(answer_obj.message, "content"):
            answer_text = answer_obj.message.content
        elif isinstance(answer_obj, str):
            answer_text = answer_obj
        else:
            log.error(f"Unexpected answer object structure for conversation_id={conversation_id}")
            raise ValueError("Unexpected answer object structure")

        clean_text = clean_response(answer_text)
        log.info(f"Returning cleaned response for conversation_id={conversation_id}")

        return ChatResponse(response=clean_text, source_docs=docs)

    except HTTPException:
        log.warning(f"HTTPException raised in chat for conversation_id={conversation_id}")
        raise
    except Exception as e:
        log.error(f"Chat error (conversation_id={conversation_id}): {e}")
        raise HTTPException(status_code=500, detail=str(e))