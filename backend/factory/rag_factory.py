from services.loader import load_files
from services.chunker import chunk_text
from services.embedder import embed_chunks
from services.vector_store import add_embeddings, query_embeddings
from services.llm import generate_answer, embed_query
from services.logger import log
import sys
sys.path.append("..")  # Add appropriate path at runtime
from services.vector_store import collection_is_empty


# class RAGPipeline:
#     def __init__(self, file_paths):
#         self.texts = load_files(file_paths)
#         self.doc_ids = file_paths

#     def ingest(self):
#         # optional clear
#         # from services.vector_store import clear_collection
#         # clear_collection()
#         for text, doc_id in zip(self.texts, self.doc_ids):
#             chunks = chunk_text(text, doc_id)
#             vectors = embed_chunks(chunks)
#             add_embeddings(vectors)
#         log.info("Ingestion complete")

#     # def query(self, query_text: str):
#     #     q_emb = embed_query(query_text)
#     #     results = query_embeddings(q_emb)
#     #     docs = []
#     #     for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
#     #         docs.append({'document': doc, 'metadata': meta})
#     #     answer = generate_answer(docs, query_text)
#     #     return answer, docs
#     def query(self, query_text: str):
#         q_emb = embed_query(query_text)
#         results = query_embeddings(q_emb)
#         docs = [{'document': d, 'metadata': m} for d, m in zip(results['documents'][0], results['metadatas'][0])]
#         answer_obj = generate_answer(docs, query_text)

#         # Extract string from answer_obj here
#         answer_text = answer_obj.message.content if hasattr(answer_obj, "message") else str(answer_obj)

#         return answer_text, docs


class RAGPipeline:
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.texts = None  # Delay loading until ingest

    def ingest(self):
        self.texts = load_files(self.file_paths)
        for text, doc_id in zip(self.texts, self.file_paths):
            chunks = chunk_text(text, doc_id)
            vectors = embed_chunks(chunks)
            add_embeddings(vectors)
        log.info("Ingestion complete")

    def query(self, query_text: str):
        q_emb = embed_query(query_text)
        results = query_embeddings(q_emb)
        docs = [{'document': d, 'metadata': m} for d, m in zip(results['documents'][0], results['metadatas'][0])]
        answer_obj = generate_answer(docs, query_text)
        answer_text = answer_obj.message.content if hasattr(answer_obj, "message") else str(answer_obj)
        return answer_text, docs