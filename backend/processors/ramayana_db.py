from backend.models.user_query import VectorDBQueryProcessor

class RamayanaDBProcessor(VectorDBQueryProcessor):
    
    def process_query(self, query: str, collection: str, vdb_name: str) -> dict:
        result = f"{vdb_name}->{collection}: Query :{query}"
        return {"answer": result}

