import argparse
import os
import uvicorn
#from app import create_app
from app import app

def main():
    parser = argparse.ArgumentParser(description="Launch the RAG chatbot service")
    parser.add_argument(
        "--mode",
        choices=["api", "ui"],
        default="api",
        help="Run as API server (FastAPI) or UI (Streamlit)",
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind the server"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    args = parser.parse_args()

    os.environ.setdefault("LOG_LEVEL", "INFO")

    if args.mode == "api":
        uvicorn.run("app:app", host=args.host, port=args.port, reload=True)
    else:
        os.system(f"streamlit run ui/streamlit_app.py --server.port {args.port}")


if __name__ == "__main__":
    main()