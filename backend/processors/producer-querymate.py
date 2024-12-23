# https://www.youtube.com/watch?v=QSW2L8dkaZk

import os
import sys
import time

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_FOLDER)

import json
import chromadb
import logging
from chromadb.utils import embedding_functions
from backend.config import Config
from backend.utils.vdb_operations import get_text_embedding

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def producer_create_embeddings(collection, json_data, batchsize=0, queue=None):
    documents = []
    metadata = []
    ids = []
    data = []

    logging.debug(f"Loading userdata :{json_data}...")
    try:
        with open(json_data, 'r') as rfd:
            data = json.load(rfd)
    except IOError as err:
        logging.debug(f"Failed to load data :{err}")
        exit(1)

    logging.debug(f"Loaded.")
    for i, row in enumerate(data, 1):
        # build id
        ids = str(i)

        # build metadata
        mdate, mtime =  row['datetime'].split()
        author = row['sender']
        if not author:
            author = ""
            
        attachment = row['attachment']
        if not attachment:
            attachment = ""
        metadata = {'date': mdate, 'time': mtime, 'Author' : author, 'attachment' : attachment}

        # build document
        documents = row['message']

        logging.debug(f"Processing Record :{i}, with doc len :{len(documents)}")

        # results = collection.get(ids=str(i))
        # if (len(results['ids']) != 0):
        #     continue
        
        logging.debug(f"Generating Embeddings with doc len :{len(documents)}")
        embeddings = []
        if len(documents) > 0:
            embeddings = get_text_embedding(documents)
        
        logging.debug(f"Updating collection...")
        if len(embeddings) > 0:
            collection.add(documents=documents, metadatas=metadata, ids=ids, embeddings=embeddings)
        else:
            dummy_embedding = [0.0] * 768
            collection.add(documents=documents, metadatas=metadata, ids=ids, embeddings=dummy_embedding)
        logging.debug(f"Updated.")

        # print(f"ids      :{ids}")
        # print(f"metadata :{metadata}")
        # print(f"docs     :{documents}")
        # print(f"embeddings len :{len(embeddings)}")
        print(f"Updated collection with Record :{i}")
        print()
        
        if (i%20 == 0):
            time.sleep(3)
    logging.debug(f"Finished Embedding csv data :{json_data}")

def server_init_croma_db(vectdb_name, coll_name):
    client = chromadb.PersistentClient(path=vectdb_name)

    # sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
    # collection = client.get_or_create_collection(name=coll_name, embedding_function=sentence_transformer_ef)
    collection = client.get_or_create_collection(name=coll_name)
    logging.debug(f"In {vectdb_name} found collection {coll_name} with documents count :{collection.count()}")
    
    return collection

def dump_collection_details(collection):
    print(collection.get())
    count = collection.count()   
    print()
    # print(f"collection count :{count}")
    print()

def delete_collection_by_name(collection_name):
    client = chromadb.Client()
    
    try:
        client.delete_collection(name=collection_name)
        # print(f"Successfully Deleted collection :{collection_name}")
    except ValueError as err:
        print(f"Collection doesn't exists :{err}")
        pass
        
    return

def main():
    vdbs_path = Config.VECTOR_DBS_PATH
    vdb_name = vdbs_path + Config.SIRIJEEVANA_VECTOR_DB_NAME
    cname = Config.SRIRIJEEVANA_COLLECTION_NAME
    udata_path = Config.USER_DATA_PATH
    parsed_data = udata_path + Config.SIRIJEEVANA_PARSED_DATA
    
    logging.debug(f"vdb_name :{vdb_name}")
    logging.debug(f"cname    :{cname}")
    logging.debug(f"parsed_data :{parsed_data}")
    collection = server_init_croma_db(vdb_name, cname)
    
    producer_create_embeddings(collection, parsed_data)
    logging.debug(f"count :{collection.count()}")
    print(f"Finished creating embeddings...")

if (__name__ == "__main__"):
    main()
