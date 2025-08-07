# from langchain.vectorstores import Chroma
# from langchain.embeddings import OllamaEmbeddings

# def get_retriever(persist_dir="vectorstore/"):
#     vectordb = Chroma(
#         persist_directory=persist_dir,
#         embedding_function=OllamaEmbeddings(model="llama3")
#     )
#     return vectordb.as_retriever(search_kwargs={"k": 4})

#----------------------------------------------
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings import SentenceTransformerEmbeddings

# def get_retriever(persist_dir="vectorstore/"):
#     embedding_function = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")
#     vectordb = Chroma(
#                 persist_directory=persist_dir,
#                 embedding_function=embedding_function
#                 )
#     return vectordb.as_retriever(search_kwargs={"k": 4})
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer, util
import torch

class RerankingRetriever:
    def __init__(self, persist_dir: str, embedding_model_name="all-mpnet-base-v2", k=4, rerank_top_k=5):
        self.k = k
        self.rerank_top_k = rerank_top_k
        self.model = SentenceTransformer(embedding_model_name)
        self.vectordb = Chroma(
            persist_directory=persist_dir,
            embedding_function=SentenceTransformerEmbeddings(model_name=embedding_model_name)
        )
        self.retriever = self.vectordb.as_retriever(search_kwargs={"k": self.k})

    def rerank_chunks(self, chunks, query):
        if not chunks:
            return []
        texts = [chunk.page_content if hasattr(chunk, "page_content") else chunk["text"] for chunk in chunks]
        chunk_embeds = self.model.encode(texts, convert_to_tensor=True)
        query_embed = self.model.encode(query, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(query_embed, chunk_embeds)[0]
        top_results = torch.topk(cosine_scores, k=min(self.rerank_top_k, len(chunks)))
        reranked = [chunks[idx] for idx in top_results.indices]
        return reranked

    def get_relevant_documents(self, query):
        initial_results = self.retriever.get_relevant_documents(query)
        return self.rerank_chunks(initial_results, query)

def get_retriever(persist_dir="vectorstore/", k=4, rerank_top_k=5):
    return RerankingRetriever(persist_dir, "all-mpnet-base-v2", k, rerank_top_k)