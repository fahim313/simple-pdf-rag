from pathlib import Path

from fastapi import FastAPI, File, UploadFile

from .ingestion import ingest_pdf
from .embeddings import generate_embeddings, model
from .database import create_vector_store, save_vector_store


app = FastAPI(
    title="Simple PDF RAG",
    description="A simple PDF-based RAG API",
    version="1.0.0",
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

    # Generate embeddings
    embeddings = generate_embeddings(result["documents"])

    # Create FAISS vector store
    vector_store = create_vector_store(
        result["documents"],
        embeddings,
        model,
    )

    # Save the vector store
    save_vector_store(vector_store)

    return {
        "message": "PDF processed successfully",
        "filename": file.filename,
        "pages": result["pages"],
        "chunks": result["chunks"],
        "embedding_dimension": len(embeddings[0]),
    }