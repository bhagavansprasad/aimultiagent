from backend.models.user_query import VectorDBQueryProcessor

class pdfDBProcessor(VectorDBQueryProcessor):
    
    async def process_query(self, query: str, collection: str) -> dict:
        # Logic specific to ChromaDB
        result = f"Processed pdf-vectorDB query result, collection :{collection}"
        return {"answer": result}
