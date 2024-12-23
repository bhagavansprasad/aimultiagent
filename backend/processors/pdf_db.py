from backend.models.user_query import VectorDBQueryProcessor

class pdfDBProcessor(VectorDBQueryProcessor):
    
    def process_query(self, query: str, collection: str, vdb_name: str) -> dict:
        # Logic specific to ChromaDB
        result = f"{vdb_name}->{collection}: Query :{query}"
        return {"answer": result}
