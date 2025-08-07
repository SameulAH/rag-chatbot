import ollama
from typing import List
from services.chunker import Chunk
import structlog
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-mpnet-base-v2")

log = structlog.get_logger()
client = ollama.Client()            # Updated import for ollama-sdk
# EMBED_MODEL = "nomic-embed-text"
EMBED_MODEL = "all-mpnet-base-v2"  # New model name for embeddings
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



# def embed_chunks(chunks: List[Chunk]) -> List[dict]:
#     texts = [c.text for c in chunks]
#     log.info("Creating embeddings batch", model=EMBED_MODEL, batch_size=len(texts))
    
#     response = client.embed(model=EMBED_MODEL, input=texts)
    
#     embeddings = response.get("embeddings")
#     if embeddings is None:
#         raise ValueError("No embeddings found in response")

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
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    results = []
    for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        results.append({
            "id": f"{chunk.metadata['doc_id']}-{idx}",
            "embedding": emb,
            "metadata": chunk.metadata,
            "text": chunk.text,
        })
    return results