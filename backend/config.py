# backend/config.py

class Config:
    # General settings
    DEBUG = True
    API_URL = "http://localhost:8000"

    VECTOR_DBS_PATH = "/home/bhagavan/vectDBs"
    
    # VectorDB connection settings
    CHROMA_DB_URI = "path/to/chroma/db"
    RAMAYANA_DB_URI = "path/to/ramayana/db"
    MAHABHARATA_DB_URI = "path/to/mahabharata/db"
    
    # Other configurations (could be secrets, logging, etc.)
    SECRET_KEY = "your_secret_key"
