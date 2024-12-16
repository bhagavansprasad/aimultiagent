from backend.models.user_query import VectorDBQueryProcessor

class RamayanaDBProcessor(VectorDBQueryProcessor):
    
    async def process_query(self, query: str, collection: str) -> dict:
        result = f"Processed RamayanaDB query result, collection :{collection}"
        return {"answer": result}

