from typing import List
from dataclasses import dataclass
import tiktoken
import structlog

log = structlog.get_logger()

# Use an encoder matching the LLM's tokenizer (e.g. OpenAI/Ollama)
ENCODER = tiktoken.get_encoding("cl100k_base")
MAX_TOKENS = 200
OVERLAP = 50

@dataclass
class Chunk:
    text: str
    metadata: dict


def chunk_text(text: str, doc_id: str) -> List[Chunk]:
    tokens = ENCODER.encode(text)
    chunks = []
    start = 0
    total = len(tokens)
    log.info("Chunking text", doc_id=doc_id, total_tokens=total)
    while start < total:
        end = min(start + MAX_TOKENS, total)
        chunk_tokens = tokens[start:end]
        chunk_str = ENCODER.decode(chunk_tokens)
        chunks.append(
            Chunk(
                text=chunk_str,
                metadata={"doc_id": doc_id, "start": start, "end": end},
            )
        )
        start += MAX_TOKENS - OVERLAP
    log.info("Generated chunks", doc_id=doc_id, chunks=len(chunks))
    return chunks