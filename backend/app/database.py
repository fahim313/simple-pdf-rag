from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from pathlib import Path


def create_vector_store(
    documents: list[Document],
    embeddings,
    embedding_model,
):
    """Create a FAISS vector store from documents and embeddings."""

    vector_store = FAISS.from_embeddings(
        text_embeddings=[
            (document.page_content, embedding)
            for document, embedding in zip(documents, embeddings)
        ],
        embedding=embedding_model,
        metadatas=[document.metadata for document in documents],
    )

    return vector_store

def save_vector_store(vector_store, path: str = "vector_store"):
    """
    Save FAISS vector store to disk.
    
    """

    Path(path).mkdir(parents=True, exist_ok=True)

    vector_store.save_local(path)