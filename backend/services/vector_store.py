import os
from chromadb import PersistentClient
from typing import List, Dict
import structlog

# Ensure the vector store directory exists

log = structlog.get_logger()

DB_DIR = "vector_store"
os.makedirs(DB_DIR, exist_ok=True)

client = PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name="documents")


def collection_exists() -> bool:
    collections = client.list_collections()
    print("Collections in DB:", collections)
    return "documents" in collections


def collection_is_empty() -> bool:
    if "documents" not in client.list_collections():
        return True
    count = collection.count()
    return count == 0

def add_embeddings(vectors: List[Dict]):
    
    log.info("Adding embeddings", count=len(vectors))
    ids = [v["id"] for v in vectors]
    embs = [v["embedding"] for v in vectors]
    metas = [v["metadata"] for v in vectors]
    docs = [v["text"] for v in vectors]
    collection.add(ids=ids, embeddings=embs, metadatas=metas, documents=docs)

def query_embeddings(query_emb: List[float], top_k: int = 5) -> Dict:
    log.info("Querying embeddings", top_k=top_k)
    return collection.query(query_embeddings=[query_emb], n_results=top_k)

def clear_collection():
    log.info("Clearing collection")
    client.delete_collection(name="documents")
