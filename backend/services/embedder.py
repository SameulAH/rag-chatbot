import ollama
from typing import List
from services.chunker import Chunk
import structlog

log = structlog.get_logger()
client = ollama.Client()            # Updated import for ollama-sdk
EMBED_MODEL = "nomic-embed-text"

# def embed_chunks(chunks: List[Chunk]) -> List[dict]:
#     texts = [c.text for c in chunks]
#     log.info("Creating embeddings batch", model=EMBED_MODEL, batch_size=len(texts))
#     embeddings = client.embed(model=EMBED_MODEL, input=texts)
#     results = []
#     for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
#         results.append({
#             "id": f"{chunk.metadata['doc_id']}-{idx}",
#             "embedding": emb,
#             "metadata": chunk.metadata,
#             "text": chunk.text,
#         })
#     return results

def embed_chunks(chunks: List[Chunk]) -> List[dict]:
    texts = [c.text for c in chunks]
    log.info("Creating embeddings batch", model=EMBED_MODEL, batch_size=len(texts))
    
    response = client.embed(model=EMBED_MODEL, input=texts)
    
    embeddings = response.get("embeddings")
    if embeddings is None:
        raise ValueError("No embeddings found in response")

    results = []
    for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        results.append({
            "id": f"{chunk.metadata['doc_id']}-{idx}",
            "embedding": emb,
            "metadata": chunk.metadata,
            "text": chunk.text,
        })
    return results