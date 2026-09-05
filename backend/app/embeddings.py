from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


class SentenceTransformerEmbeddings(Embeddings):
    """
    Adapter for using SentenceTransformer with LangChain.
    
    """

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple documents."""

        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        """
        Generate embedding for a single query.
        
        """

        embedding = model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()


embedding_model = SentenceTransformerEmbeddings()


def generate_embeddings(chunks):
    """
    Convert document chunks into numerical vectors.
    
    """

    texts = [chunk.page_content for chunk in chunks]

    return embedding_model.embed_documents(texts)