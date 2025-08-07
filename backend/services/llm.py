# import ollama
# from services.prompt import build_prompt
# from services.logger import log

# LLM_MODEL = "llama3"            # or "llama2-chat" if that’s what you pulled
# EMBED_MODEL = "nomic-embed-text"  # replace with whatever embedding model you actually have

# def embed_query(text: str) -> list[float]:
#     log.info("Embedding query")
#     response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
#     return response["embedding"]

# def generate_answer(chunks: list, query: str, stream: bool = False):
#     prompt = build_prompt(chunks, query)
#     log.info("Sending prompt to LLM", model=LLM_MODEL)
#     messages = [
#         {"role": "system", "content": prompt},
#         {"role": "user", "content": query}
#     ]
#     return ollama.chat(model=LLM_MODEL, messages=messages, stream=stream)



from sentence_transformers import SentenceTransformer
from services.prompt import build_prompt
from services.logger import log
import ollama  # still used for LLM chat

LLM_MODEL = "llama3"                      # You can keep using Ollama for chat
EMBED_MODEL = "all-mpnet-base-v2"         # New model name for embeddings

# Load the embedding model once
embedding_model = SentenceTransformer(EMBED_MODEL)

def embed_query(text: str) -> list[float]:
    log.info("Embedding query using all-mpnet-base-v2")
    return embedding_model.encode(text).tolist()

def generate_answer(chunks: list, query: str, stream: bool = False):
    prompt = build_prompt(chunks, query)
    log.info("Sending prompt to LLM", model=LLM_MODEL)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": query}
    ]
    return ollama.chat(model=LLM_MODEL, messages=messages, stream=stream)
