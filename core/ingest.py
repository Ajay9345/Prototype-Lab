import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ── Constants ─────────────────────────────────────────────────────────────────
DATA_PATH      = "data"
VECTOR_DB_PATH = "faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE     = 500
CHUNK_OVERLAP  = 50


def ingest_data() -> None:
    """
    Load text documents from the data/ folder, split them into chunks,
    create vector embeddings, and save the FAISS index to disk.

    Run this script once before starting the app, or whenever the
    source documents change.
    """
    # Create data directory if it doesn't exist yet
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"Created '{DATA_PATH}' directory. Add .txt files there and re-run.")
        return

    # ── Step 1: Load documents ────────────────────────────────────────────────
    print("Loading documents...")
    loader    = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()

    if not documents:
        print("No .txt documents found in the data/ directory.")
        return

    print(f"Loaded {len(documents)} document(s).")

    # ── Step 2: Split into smaller chunks ────────────────────────────────────
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunk(s).")

    # ── Step 3: Create embeddings and build FAISS index ───────────────────────
    print("Creating embeddings (this may take a moment)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Building vector store...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(VECTOR_DB_PATH)

    print(f"Vector store saved to '{VECTOR_DB_PATH}'. Ingestion complete.")


if __name__ == "__main__":
    ingest_data()
