from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from .ingestion import ingest_pdf

app = FastAPI(
    title="Simple PDF RAG",
    description="A simple PDF-based RAG API",
)


# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {
        "message": "Simple PDF RAG API is running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return {
            "error": "Only PDF files are allowed"
        }

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Ingest PDF
    result = ingest_pdf(str(file_path))

    return {
        "message": "PDF uploaded and processed successfully",
        "filename": file.filename,
        "pages": result["pages"],
        "chunks": result["chunks"],
    }