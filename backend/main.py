import os
from fastapi import FastAPI, Query, Body, Request
from typing import List, Dict
from pydantic import BaseModel
from backend.config import Config
import chromadb 
from backend.models.user_query import VectorDBQueryProcessor
from backend.utils.query_processor_factory import QueryProcessorFactory
from pdbwhereami import whereami
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()
vector_dbs_path = Config.VECTOR_DBS_PATH

def get_vect_dbs_list(vect_path):
    whereami()
    return os.listdir(vect_path)

def get_collections_list(vdb_name, vdb_path):
    whereami()
    client = chromadb.PersistentClient(path=f"{vdb_path}/{vdb_name}")

    collection_list = [collection.name for collection in client.list_collections()]

    return collection_list

@app.get("/get_vectordbs")
def get_vectordbs() -> Dict[str, List[str]]:
    whereami()
    
    vdb_list = get_vect_dbs_list(vector_dbs_path)
    
    return {"vectordbs": vdb_list}

@app.get("/get_collections")
def get_collections(vdb_name: str = Query(..., description="Name of the VectorDB")) -> List[str]:
    whereami()
    
    collections_list = get_collections_list(vdb_name, vector_dbs_path)
    
    return collections_list

class UserQuery(BaseModel):
    query: str

@app.post("/user_query")
def user_query(request: Request, query: UserQuery = Body(...)):
    whereami()
    
    raw_payload = request.json()
    whereami(f"raw_payload :{raw_payload}")
    vector_db_name = raw_payload.get("vdb_name")
    collection = raw_payload.get("collection_name")
    whereami(f"vector_db_name :{vector_db_name}")
    whereami(f"collection :{collection}")
    
    # Get the correct processor based on the vector_db_name
    processor: VectorDBQueryProcessor = QueryProcessorFactory.get_processor(vector_db_name)
    
    # Process the query and get the answer
    processed_query = processor.process_query(query.query, collection, vector_db_name)
    
    print(f"Payload :{raw_payload}")
    return processed_query