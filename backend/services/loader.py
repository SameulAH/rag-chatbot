import os
from typing import List
from docx import Document
import structlog
import pdfplumber
log = structlog.get_logger()


def _load_pdf(path: str) -> str:
    with pdfplumber.open(path) as pdf:
        text_pages = []
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text() or ""
            text_pages.append(page_text)
    return "\n".join(text_pages)

def load_files(paths: List[str]) -> List[str]:
    texts = []
    for path in paths:
        if not os.path.isfile(path):
            log.error("File not found", path=path)
            raise FileNotFoundError(f"File not found: {path}")
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            texts.append(_load_pdf(path))
        elif ext == ".docx":
            texts.append(_load_docx(path))
        elif ext == ".txt":
            with open(path, encoding="utf-8") as f:
                texts.append(f.read())
        else:
            log.error("Unsupported file type", path=path, ext=ext)
            raise ValueError(f"Unsupported file type: {ext}")
    return texts


# def _load_pdf(path: str) -> str:
#     text_pages = []
#     try:
#         with PDF(path) as pdf:
#             for i, page in enumerate(pdf.pages):
#                 page_text = page.extract_text()
#                 if not page_text:
#                     log.warning("Empty PDF page", path=path, page=i)
#                     page_text = ""
#                 text_pages.append(page_text)
#     except Exception as e:
#         log.error("PDF load error", path=path, error=str(e))
#         raise
#     return "\n".join(text_pages)


def _load_docx(path: str) -> str:
    try:
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        log.error("DOCX load error", path=path, error=str(e))
        raise