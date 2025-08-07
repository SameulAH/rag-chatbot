\documentclass{article}
\usepackage{geometry}
\usepackage{longtable}
\usepackage{hyperref}
\geometry{margin=1in}

\title{RAG-Based Conversational AI Infrastructure}
\author{}
\date{}

\begin{document}

\maketitle

\section*{Overview}

This project provides an AI-powered chatbot backend infrastructure using Retrieval-Augmented Generation (RAG). It supports:

\begin{itemize}
    \item Document ingestion (PDFs)
    \item Vector embeddings using \texttt{all-mpnet-base-v2}
    \item Vector storage with Chroma
    \item Natural language querying with \texttt{llama3} LLM
    \item REST API built with FastAPI
    \item Client frontend using Streamlit
\end{itemize}

The system supports multi-turn conversations with conversation ID tracking to avoid redundant ingestion.

\section*{Features}

\begin{itemize}
    \item Upload and ingest documents via API
    \item Persistent vector store with Chroma
    \item Embedding using Sentence Transformers (\texttt{all-mpnet-base-v2})
    \item Generation using \texttt{llama3} language model
    \item Async pipeline initialization and ingestion caching
    \item Conversation session management to avoid repeated ingestion
    \item Logging for debugging and tracing
    \item File upload and storage handling
\end{itemize}

\section*{Tool Stack}

\begin{longtable}{|l|l|}
\hline
\textbf{Component} & \textbf{Technology / Model} \\
\hline
Backend Framework & FastAPI \\
Async Concurrency & asyncio \\
Vector Store & Chroma \\
Embedding Model & all-mpnet-base-v2 \\
Language Model (LLM) & llama3 \\
Data Validation & Pydantic \\
File \& Storage & Python \texttt{os}, \texttt{shutil} \\
Logging & Custom logger (\texttt{services.logger}) \\
ASGI Server & Uvicorn \\
Client UI & Streamlit \\
HTTP Client & Requests (Streamlit) \\
\hline
\end{longtable}

\section*{Architecture \& Workflow}

\begin{enumerate}
    \item \textbf{Document ingestion:}  
    Uploaded documents (PDFs) are saved, embedded using the embedding model, and stored in Chroma vector DB.
    
    \item \textbf{Pipeline Initialization:}  
    A global RAG pipeline instance is initialized asynchronously on startup or on-demand, avoiding repeated ingestion.
    
    \item \textbf{Chat Requests:}  
    Each chat request includes a conversation ID to track sessions. The pipeline queries the vector store and LLM to generate contextual responses.
    
    \item \textbf{Ingestion Caching:}  
    Ingestion results are cached in memory to avoid redundant ingestion for the same session. The pipeline reinitializes only after a time-to-live (TTL) expires.
\end{enumerate}

\section*{Getting Started}

\begin{enumerate}
    \item Clone the repository.
    \item Install dependencies (e.g., \texttt{fastapi}, \texttt{uvicorn}, \texttt{pydantic}, \texttt{chromadb}, \texttt{sentence-transformers}, \texttt{streamlit}).
    \item Run backend server with Uvicorn.
    \item Launch Streamlit client for UI interaction.
\end{enumerate}

\section*{Future Improvements}

\begin{itemize}
    \item Persist ingestion cache to disk or database for true persistence across restarts.
    \item Add intent classification to detect ingestion commands in chat.
    \item Enhance session tracking with Redis or database.
    \item Secure file uploads and API endpoints.
\end{itemize}

\end{document}
