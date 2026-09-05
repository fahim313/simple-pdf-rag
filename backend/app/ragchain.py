import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from .database import load_vector_store
from .embeddings import embedding_model


load_dotenv()


# model

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


# Prompt
prompt = ChatPromptTemplate.from_template(
    """
    Answer the question using only the context provided below.

    If the answer is not available in the context, say:
    "I could not find the answer in the PDF."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
)


def ask_question(question: str, k: int = 3):
    """
    Retrieve relevant chunks and generate an answer.
    
    """

    # Load FAISS vector store
    vector_store = load_vector_store(
    embedding_model=embedding_model,
)

    # Retrieve relevant documents
    documents = vector_store.similarity_search(
        question,
        k=k,
    )

    # Combine retrieved chunks
    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # Create prompt
    messages = prompt.format_messages(
        context=context,
        question=question,
    )

    # Generate answer
    response = llm.invoke(messages)

    return {
        "answer": response.content,
        "sources": [
            {
                "content": document.page_content,
                "metadata": document.metadata,
            }
            for document in documents
        ],
    }