import ollama
from services.prompt import build_prompt
from services.logger import log

LLM_MODEL = "llama3"            # or "llama2-chat" if that’s what you pulled
EMBED_MODEL = "nomic-embed-text"  # replace with whatever embedding model you actually have

def embed_query(text: str) -> list[float]:
    log.info("Embedding query")
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]

def generate_answer(chunks: list, query: str, stream: bool = False):
    prompt = build_prompt(chunks, query)
    log.info("Sending prompt to LLM", model=LLM_MODEL)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": query}
    ]
    return ollama.chat(model=LLM_MODEL, messages=messages, stream=stream)
