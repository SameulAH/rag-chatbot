# RAG-Based Conversational AI Infrastructure

## Overview

This project provides an AI-powered chatbot backend infrastructure using Retrieval-Augmented Generation (RAG). It supports document ingestion, vector embeddings, and natural language querying to create intelligent conversational experiences.

### Key Capabilities
- 📄 Document ingestion (PDFs)
- 🔍 Vector embeddings using `all-mpnet-base-v2`
- 💾 Vector storage with Chroma
- 🤖 Natural language querying with `llama3` LLM
- 🚀 REST API built with FastAPI
- 💻 Client frontend using Streamlit

The system supports multi-turn conversations with conversation ID tracking to avoid redundant ingestion and provides efficient session management.

## ✨ Features

- **Document Processing**: Upload and ingest documents via REST API
- **Persistent Storage**: Vector store with Chroma for document embeddings
- **Smart Embeddings**: Sentence Transformers using `all-mpnet-base-v2` model
- **Advanced Generation**: `llama3` language model for contextual responses
- **Async Architecture**: Pipeline initialization and ingestion caching
- **Session Management**: Conversation tracking to avoid repeated ingestion
- **Comprehensive Logging**: Debug and trace capabilities
- **File Handling**: Robust upload and storage management

## 🛠️ Technology Stack

| Component | Technology / Model |
|-----------|-------------------|
| **Backend Framework** | FastAPI |
| **Async Concurrency** | asyncio |
| **Vector Store** | Chroma |
| **Embedding Model** | all-mpnet-base-v2 |
| **Language Model (LLM)** | llama3 |
| **Data Validation** | Pydantic |
| **ASGI Server** | Uvicorn |
| **Client UI** | Streamlit |
| **HTTP Client** | Requests (in Streamlit) |

## 🏗️ Architecture & Workflow

### 1. Document Ingestion
Uploaded documents (PDFs) are processed through the following pipeline:
- Documents are saved to local storage
- Content is extracted and chunked
- Embeddings are generated using the embedding model
- Vectors are stored in Chroma vector database

### 2. Pipeline Initialization
- Global RAG pipeline instance initialized asynchronously
- On-demand startup or initialization
- Prevents repeated ingestion through caching mechanisms

### 3. Chat Request Processing
- Each request includes conversation ID for session tracking
- Pipeline queries vector store for relevant context
- LLM generates contextual responses based on retrieved information

### 4. Ingestion Caching
- Results cached in memory to avoid redundant processing
- Session-based caching for same conversation ID
- Time-to-live (TTL) expiration for cache invalidation

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Required dependencies (see installation steps)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag-conversational-ai
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn pydantic chromadb sentence-transformers streamlit requests
   ```

3. **Run the backend server**
   ```bash
   uvicorn main:app --reload
   ```

4. **Launch the Streamlit client**
   ```bash
   streamlit run streamlit_app.py
   ```

### Usage

1. Access the Streamlit interface in your browser (typically `http://localhost:8501`)
2. Upload PDF documents through the interface
3. Start conversing with your documents using natural language queries
4. The system will provide contextual responses based on the uploaded content

## 📁 Project Structure

```
RAG_APP/
├── venv/                          # Virtual environment
├── rag-chatbot/
│   └── backend/
│       ├── __pycache__/           # Python cache files
│       ├── api/
│       │   ├── __pycache__/
│       │   ├── temp/
│       │   ├── chat.py            # Chat API endpoints
│       │   ├── pipeline_state.json # Pipeline state configuration
│       │   └── routes.py          # API route definitions
│       ├── backend1.temp/
│       │   └── sampledoc.pdf     # Sample document
│       ├── data/                  # Data storage directory
│       ├── factory/
│       │   ├── __pycache__/
│       │   └── rag_factory.py    # RAG pipeline factory
│       ├── services/
│       │   ├── __pycache__/
│       │   ├── chunker.py        # Document chunking service
│       │   ├── embedder.py       # Embedding generation service
│       │   ├── ingest.py         # Document ingestion service
│       │   ├── llm.py            # Language model service
│       │   ├── loader.py         # Document loading service
│       │   ├── logger.py         # Logging utilities
│       │   ├── prompt.py         # Prompt templates
│       │   ├── retrieval.py      # Document retrieval service
│       │   └── vector_store.py   # Vector database operations
│       ├── vector_store/
│       │   └── 66c07bcd-9ed6-4b05-b30e-da7a159b9780/
│       │       └── chroma.sqlite3 # Chroma vector database
│       └── app.py                # Main FastAPI application
├── ui/
│   └── streamlit_app.py          # Streamlit frontend client
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
├── .gitattributes               # Git attributes configuration
└── .gitignore                   # Git ignore rules
```

## 🔮 Future Improvements

- [ ] **Persistent Caching**: Implement disk or database-based ingestion cache for true persistence across restarts
- [ ] **Intent Classification**: Add detection for ingestion commands within chat interface
- [ ] **Enhanced Session Tracking**: Integrate Redis or database for robust session management
- [ ] **Security Enhancements**: Implement secure file uploads and API endpoint protection
- [ ] **Multi-format Support**: Extend beyond PDFs to support various document formats
- [ ] **User Authentication**: Add user management and access control
- [ ] **Performance Monitoring**: Implement metrics and performance tracking
- [ ] **Scalability**: Add support for distributed processing and load balancing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions, please open an issue in the GitHub repository or contact the development team.

---

*Built with ❤️ using FastAPI, Streamlit, and state-of-the-art AI technologies*