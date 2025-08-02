from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings

def get_retriever(persist_dir="vectorstore/"):
    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=OllamaEmbeddings(model="llama3")
    )
    return vectordb.as_retriever(search_kwargs={"k": 4})
