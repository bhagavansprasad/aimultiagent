from backend.models.user_query import VectorDBQueryProcessor

class MahabharataDBProcessor(VectorDBQueryProcessor):
    
    async def process_query(self, query: str, collection: str) -> dict:
        # Logic specific to Mahabharata DB
        result = f"Processed MahabharataDB query result, collection :{collection}"
        return {"answer": result}
