from abc import ABC, abstractmethod

class VectorDBQueryProcessor(ABC):
    
    @abstractmethod
    async def process_query(self, query: str, collection: str) -> dict:
        pass
