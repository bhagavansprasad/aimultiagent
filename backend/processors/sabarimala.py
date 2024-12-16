from backend.models.user_query import VectorDBQueryProcessor

class SabarimalaDBProcessor(VectorDBQueryProcessor):
    
    async def process_query(self, query: str, collection: str) -> dict:
        result = f"Processed Sabarimala query result, collection :{collection}"
        return {"answer": result}

