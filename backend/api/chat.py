from fastapi import APIRouter, Body
from app.core.rag_factory import RAGFactory
from pydantic import BaseModel

router = APIRouter()
rag = RAGFactory()
qa_chain = rag.get_rag_chain()

@router.post("/ask")
def ask_rag(query: str = Body(...)):
    result = qa_chain.run(query)
    return {"answer": result}

class QueryRequest(BaseModel):
    query: str

@router.post("/ask")
def ask_rag(payload: QueryRequest):
    ...