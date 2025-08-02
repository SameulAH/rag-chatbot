import os
import shutil
import uuid
import asyncio
from typing import List, Optional

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from factory.rag_factory import RAGPipeline
from services.logger import log
from typing import Optional

router = APIRouter()

# Async lock to protect the pipeline shared mutable state
pipeline_lock = asyncio.Lock()

# Shared RAGPipeline instance
pipeline: Optional[RAGPipeline] = None

# Base directory for saving temporary uploaded files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.makedirs(TEMP_DIR, exist_ok=True)


class ChatRequest(BaseModel):
    query: str



class ChatResponse(BaseModel):
    response: str
    source_docs: Optional[List[dict]] = None  # or remove entirely if unused

# class ChatResponse(BaseModel):
#     response: str
#     source_docs: List


class IngestPathsRequest(BaseModel):
    file_paths: List[str]


async def save_upload_files(files: List[UploadFile]) -> List[str]:
    """Save uploaded files to TEMP_DIR; add uuid suffix if file exists."""
    saved_paths = []
    for file in files:
        filename = file.filename
        dest_path = os.path.join(TEMP_DIR, filename)

        # Avoid overwrite
        if os.path.exists(dest_path):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{uuid.uuid4().hex}{ext}"
            dest_path = os.path.join(TEMP_DIR, filename)

        # Save the file (sync I/O inside async function is okay here)
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file.file.close()

        if not os.path.exists(dest_path):
            log.error(f"Failed to save file: {dest_path}")
            raise HTTPException(status_code=500, detail=f"Failed to save file {filename}")

        log.info(f"Saved uploaded file to: {dest_path}")
        saved_paths.append(dest_path)
    return saved_paths


@router.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    """
    Upload files and save them.
    Returns the list of saved file paths.
    """
    saved_paths = await save_upload_files(files)
    log.info("Files uploaded", files=saved_paths)
    return {"saved_files": saved_paths}


# @router.post("/ingest")
# async def ingest_uploaded(files: List[UploadFile] = File(...)):
#     """
#     Upload files, save, initialize pipeline, and ingest.
#     """
#     global pipeline
#     try:
#         saved_paths = await save_upload_files(files)
#         async with pipeline_lock:
#             pipeline = RAGPipeline(saved_paths)
#             pipeline.ingest()
#         log.info("Ingestion completed", files=saved_paths)
#         return {"status": "ingested", "files": saved_paths}
#     except Exception as e:
#         log.error("Ingestion error", error=str(e))
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest")
async def ingest_uploaded(files: List[UploadFile] = File(...)):
    global pipeline
    try:
        saved_paths = await save_upload_files(files)
        log.info(f"Saved paths for ingestion: {saved_paths}")
        async with pipeline_lock:
            pipeline = RAGPipeline(saved_paths)  # Must pass paths, not UploadFile objects
            pipeline.ingest()
        log.info("Ingestion completed", files=saved_paths)
        return {"status": "ingested", "files": saved_paths}
    except Exception as e:
        log.error("Ingestion error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/paths")
async def ingest_paths(request: IngestPathsRequest):
    """
    Ingest from existing file paths.
    """
    global pipeline
    try:
        abs_paths = []
        for path in request.file_paths:
            abs_path = path if os.path.isabs(path) else os.path.join(TEMP_DIR, path)
            if not os.path.exists(abs_path):
                raise HTTPException(status_code=400, detail=f"File does not exist: {abs_path}")
            abs_paths.append(abs_path)

        async with pipeline_lock:
            pipeline = RAGPipeline(abs_paths)
            pipeline.ingest()
        log.info("Ingestion from paths completed", files=abs_paths)
        return {"status": "ingested", "files": abs_paths}
    except HTTPException:
        raise
    except Exception as e:
        log.error("Ingestion error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))



def format_answer_with_refs(answer_text: str, docs: list) -> str:
    refs = []
    seen = set()
    for doc in docs:
        meta = doc.get("metadata", {})
        doc_id = meta.get("doc_id", "unknown_doc")
        start = meta.get("start")
        end = meta.get("end")
        label = f"{os.path.basename(doc_id)}:{start}-{end}" if start is not None and end is not None else os.path.basename(doc_id)
        if label not in seen:
            refs.append(label)
            seen.add(label)

    if not refs:
        return answer_text.strip()

    # Compose reference list
    refs_text = "\n\nReferences:\n" + "\n".join(f"[{i+1}] {ref}" for i, ref in enumerate(refs))
    return answer_text.strip() + refs_text

# @router.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(req: ChatRequest):
#     try:
#         answer, docs = RAGPipeline.query(req.query)
#         formatted_answer = format_answer_with_refs(answer, docs)
#         return {
#             "response": formatted_answer,
#             "source_docs": docs  # frontend may choose to show/hide this
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    global pipeline
    if pipeline is None:
        raise HTTPException(status_code=400, detail="Pipeline not initialized. Call /ingest first.")

    try:
        answer_obj, _docs = pipeline.query(request.query)
        
        # Extract main LLM response text
        if hasattr(answer_obj, "message") and hasattr(answer_obj.message, "content"):
            answer_text = answer_obj.message.content.strip()
        elif isinstance(answer_obj, str):
            answer_text = answer_obj.strip()
        else:
            raise ValueError("Unexpected answer object structure")

        # Return only the main answer text
        return {
            "response": answer_text
        }
    except Exception as e:
        log.error("Chat error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

## latest one
# @router.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     global pipeline
#     if pipeline is None:
#         raise HTTPException(status_code=400, detail="Pipeline not initialized. Call /ingest first.")

#     try:
#         answer_obj, docs = pipeline.query(request.query)
#         # Extract string from answer_obj
#         if hasattr(answer_obj, "message") and hasattr(answer_obj.message, "content"):
#             answer_text = answer_obj.message.content
#         elif isinstance(answer_obj, str):
#             answer_text = answer_obj
#         else:
#             raise ValueError("Unexpected answer object structure")

#         return {"response": answer_text, "source_docs": docs}
#     except Exception as e:
#         log.error("Chat error", error=str(e))
#         raise HTTPException(status_code=500, detail=str(e))
