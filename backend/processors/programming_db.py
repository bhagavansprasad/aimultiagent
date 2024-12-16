from backend.models.user_query import VectorDBQueryProcessor

class ProgrammingDBProcessor(VectorDBQueryProcessor):
    
    async def process_query(self, query: str, collection: str) -> dict:
        result = f"Processed Programming query result, collection :{collection}"
        return {"answer": result}

