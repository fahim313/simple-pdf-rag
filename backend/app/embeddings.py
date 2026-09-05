from sentence_transformers import SentenceTransformer 

# Load the model 
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def generate_embeddings(chunks):
    """
    Convert document chunks into numerical vectors.
    
    """

    texts = [chunk.page_content for chunk in chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings