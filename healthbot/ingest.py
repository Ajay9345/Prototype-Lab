import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def ingest_data():
    data_path = "data"
    vector_db_path = "faiss_index"
    
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        print(f"Created {data_path} directory. Please add text files there.")
        return

    print("Loading documents...")
    loader = DirectoryLoader(data_path, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print("No documents found in data directory.")
        return

    print(f"Loaded {len(documents)} documents.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    print(f"Split into {len(texts)} chunks.")
    
    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    print("Creating vector store...")
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(vector_db_path)
    
    print(f"Vector store saved to {vector_db_path}")

if __name__ == "__main__":
    ingest_data()
