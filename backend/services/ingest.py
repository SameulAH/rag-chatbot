import os
import time

VECTOR_STORE_PATH = "rag-chatbot\backend\vector_store\66c07bcd-9ed6-4b05-b30e-da7a159b978a\index_metadata.pickle"  # Adjust this path to your index file

def ingest_documents():
    """
    Add your ingestion logic here:
    Load documents, chunk them, embed, and store into vector DB.
    """
    print("🚀 Ingesting documents...")
    # Your actual ingestion logic here
    # e.g., doc_loader.load() → chunk → embed → vectorstore.save()
    pass


def is_ingestion_needed():
    """
    Logic to determine if ingestion is needed:
    Returns True if the vector store doesn't exist or is outdated.
    """
    if not os.path.exists(VECTOR_STORE_PATH):
        return True

    # Optionally: check if docs are newer than index
    index_mtime = os.path.getmtime(VECTOR_STORE_PATH)
    docs_mtime = max(
        os.path.getmtime(os.path.join("docs", f))
        for f in os.listdir("docs") if f.endswith(".pdf") or f.endswith(".txt")
    )

    return docs_mtime > index_mtime
