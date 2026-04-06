"""
ingest.py — convenience wrapper at the project root.
Delegates to core/ingest.py so you can run:  python ingest.py
"""
from core.ingest import ingest_data

if __name__ == "__main__":
    ingest_data()
