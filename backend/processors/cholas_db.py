from backend.models.user_query import VectorDBQueryProcessor

class CholasDBProcessor(VectorDBQueryProcessor):
    
    async def process_query(self, query: str, collection: str) -> dict:
        result = f"Processed Cholas query result, collection :{collection}"
        return {"answer": result}
