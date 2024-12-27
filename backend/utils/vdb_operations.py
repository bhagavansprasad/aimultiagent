import logging
import chromadb
from vertexai.language_models import TextEmbeddingModel
import os
from backend.config import Config

class VDBOperations():
    # vectory DB collection obj
    vdb_collection = None

    # cache collection obj
    cache_collection = None

    vdb_name = None
    coll_name = None
    
    # Cache vector DB
    vdbs_path = Config.VECTOR_DBS_PATH
    cache_vdbname = vdbs_path + Config.VECTOR_CACHE_DB
    cache_collname = Config.CACHE_COLLECTION
    
    def __init__(self, vdb_name, cname):
        self.vdb_name = vdb_name
        self.coll_name = cname
       
        self.vdb_collection = self.get_or_create_vector_db(vdb_name=vdb_name, cname=cname)
        self.cache_collection = self.get_or_create_vector_db(vdb_name=self.cache_vdbname, cname=self.cache_collname)
    
    def get_or_create_vector_db(self, vdb_name, cname):
        logging.debug(f"Get collection Object vdb: {vdb_name}, collection :{cname}")

        client = chromadb.PersistentClient(path=vdb_name)
        collection = client.get_or_create_collection(name=cname)

        return collection    

    def get_embeddings_from_cache(self, text):
        count = self.cache_collection.count()
        logging.debug(f"Checking in cache '{self.cache_collname}' doc count :{count}")
        logging.debug(f"Text len: {len(text)},  text :'{text}")
        
        results = self.cache_collection.get(ids=[f'{text}'], include=["documents", "metadatas", "embeddings"])
        
        if (len(results['ids'])):
            logging.debug(f"Found in cache...")
            return results['embeddings']
        
        logging.debug(f"No cache found...Generating")

        text_embedding_model = TextEmbeddingModel.from_pretrained(Config.TEXT_EMBEDDING_MODEL)
        embeddings = text_embedding_model.get_embeddings([text])
        embedding_values = embeddings[0].values
        logging.debug(f"Generated embedding :{embedding_values[:5]}...")
        logging.debug(f"Caching Embeddings...")
        
        self.cache_collection.upsert(ids=[text], documents=[text], metadatas=[{'text': text}], embeddings=embedding_values)
        logging.debug(f"Cached.")
        return embedding_values
        
    def dump_search_results(self, query_results):
        ids = query_results['ids'][0]
        docs = query_results['documents'][0]
        distances = query_results['distances'][0]
        
        for i, (id, doc, distance) in enumerate(zip(ids, docs, distances), 1):
            print(f"{i}. ID: {id}")
            print(f"doc :{doc}")
            print(f"distance :{distance}")
            print()
        return 0

    def get_text_embedding(self, text, output_dimensionality=None):
        logging.debug(f"Generating embeddings for text of length: {len(text)}")
        
        embeddings = self.get_embeddings_from_cache(text)
        
        # text_embedding_model = TextEmbeddingModel.from_pretrained(Config.TEXT_EMBEDDING_MODEL)
        # embeddings = text_embedding_model.get_embeddings([text], output_dimensionality=output_dimensionality)
        # embedding_values = embeddings[0].values
        # logging.debug(f"embedding :{embedding_values[:5]}...")
        
        return embeddings

    def vdb_query(self, query, n_results=30):
        query_embedding = self.get_text_embedding(query)
        
        retval = self.vdb_collection.query(query_embeddings=query_embedding, n_results=n_results)
        logging.debug(f"Got Results len :{len(retval)}")
        
        ids = [[]]
        documents = [[]]
        distances = [[]]
        
        for i, id in enumerate(retval['ids'][0]):
            ids[0].append(retval['ids'][0][i])
            documents[0].append(retval['documents'][0][i])
            distances[0].append(retval['distances'][0][i])
            
            # if (i == n_results-1):
            #     break
        
        return {'ids': ids, 'documents': documents, 'distances': distances}

    def vdb_get_documents_by_query(self, query):
        count = self.vdb_collection.count()
        logging.debug(f"Found the collection '{self.coll_name}' with document count :{count}")

        results = self.vdb_query(query=query)
        # dump_search_results(results)

        context = "\n\n".join(results["documents"][0])
        max_tokens = Config.MAX_TOKENS 
        context = context[:max_tokens]
            
        return context

    def vdb_get_stats(self):
        count = self.vdb_collection.count()
        logging.debug(f"Found the collection '{self.coll_name}' with document count :{count}")
        data = self.vdb_collection.get(include=['metadatas'])
        
        # mdata = data['metadatas']
        # # print(mdata)
        # print(type(mdata))
        # context = []
        
        # for d in data['metadatas']:
        #     author = d['Author']
        #     attachment = d['attachment'] if len(d['attachment']) > 0 else "None"
        #     context.append(f"'{author}, {attachment}'")
        
        return data['metadatas']

