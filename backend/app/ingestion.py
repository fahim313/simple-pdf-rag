# PDF ingestion  

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 


def ingest_pdf(file_path:str):
    """
    Ingests a PDF file and returns the loaded documents.
    """
    # load pdf 
    documents = PyPDFLoader(file_path).load()
    
    # split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size =1000,
        chunk_overlap = 150,
        
    )
    chunks = text_splitter.split_documents(documents)
    
    return {
        "pages":len(documents),
        "chunks": len(chunks),
        "documents":chunks
    }