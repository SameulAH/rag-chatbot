from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog
from services.logger import configure_logging
from api.routes import router 

# Configure structured logging
configure_logging()
log = structlog.get_logger()

app = FastAPI(title="RAG Chatbot")

# CORS (tighten in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.on_event("startup")
def on_startup():
    log.info("Application startup complete")

@app.on_event("shutdown")
def on_shutdown():
    log.info("Application shutdown")