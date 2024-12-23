# backend/config.py

class Config:
    # General settings
    DEBUG = True
    API_URL = "http://localhost:8000"
    
    # Vector DBs path
    VECTOR_DBS_PATH = "/home/bhagavan/vectDBs/"
    
    # Cache VDB details
    VECTOR_CACHE_DB = "cache-vdb"
    CACHE_COLLECTION = "cache-collection"
    
    # Model details
    TEXT_EMBEDDING_MODEL = "text-embedding-004"
    GEMINI_MODEL = "gemini-1.5-flash"
    
    MAX_TOKENS = 4096

    # User data path    
    USER_DATA_PATH = "/home/bhagavan/userdata/"

    # Sirijeevana details
    SIRIJEEVANA_ATTACHMENTS = "sirijeevana/attachments/"
    SIRIJEEVANA_DATA = "sirijeevana/sirijeevana.txt"
    SIRIJEEVANA_PARSED_DATA = "sirijeevana/sirijeevana.json"
    SIRIJEEVANA_VECTOR_DB_NAME = "sirijeevana-vdb"
    SRIRIJEEVANA_COLLECTION_NAME = "sirijeevana"
    
