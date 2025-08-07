# import argparse
# import os
# import uvicorn
# #from app import create_app
# from app import app

# def main():
#     parser = argparse.ArgumentParser(description="Launch the RAG chatbot service")
#     parser.add_argument(
#         "--mode",
#         choices=["api", "ui"],
#         default="api",
#         help="Run as API server (FastAPI) or UI (Streamlit)",
#     )
#     parser.add_argument(
#         "--host", default="0.0.0.0", help="Host to bind the server"
#     )
#     parser.add_argument("--port", type=int, default=8000, help="Port number")
#     args = parser.parse_args()

#     os.environ.setdefault("LOG_LEVEL", "INFO")

#     if args.mode == "api":
#         uvicorn.run("app:app", host=args.host, port=args.port, reload=True)
#     else:
#         os.system(f"streamlit run ui/streamlit_app.py --server.port {args.port}")


# if __name__ == "__main__":
#     main()

import argparse
import os
import uvicorn
import sys

# Import your app (FastAPI) and ingestion logic
from app import app
from services.ingest import ingest_documents, is_ingestion_needed


def main():
    parser = argparse.ArgumentParser(description="Launch the RAG chatbot service")

    # Existing arguments
    parser.add_argument(
        "--mode",
        choices=["api", "ui"],
        default="api",
        help="Run as API server (FastAPI) or UI (Streamlit)",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server")
    parser.add_argument("--port", type=int, default=8000, help="Port number")

    # ✅ New ingestion-related arguments
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Force re-ingestion of all documents before starting the server",
    )
    parser.add_argument(
        "--auto-ingest",
        action="store_true",
        help="Automatically ingest only if needed (e.g., index missing or outdated)",
    )

    args = parser.parse_args()
    os.environ.setdefault("LOG_LEVEL", "INFO")

    # Handle ingestion
    if args.ingest:
        print("🔁 Forcing full ingestion of documents...")
        ingest_documents()
    elif args.auto_ingest:
        print("🔍 Checking if ingestion is needed...")
        if is_ingestion_needed():
            print("✅ Ingestion needed. Running ingestion now...")
            ingest_documents()
        else:
            print("✅ Ingestion not needed. Continuing...")

    # Start API or UI
    if args.mode == "api":
        uvicorn.run("app:app", host=args.host, port=args.port, reload=True)
    else:
        os.system(f"streamlit run ui/streamlit_app.py --server.port {args.port}")


if __name__ == "__main__":
    main()
