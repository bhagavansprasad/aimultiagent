from abc import ABC, abstractmethod

class VectorDBQueryProcessor(ABC):
    
    @abstractmethod
    def process_query(self, query: str) -> dict:
        pass

    @abstractmethod
    def get_group_members(self, vdb_name, collection_name) -> dict:
        pass
    
    @abstractmethod
    def get_stats(self, vdb_name, collection_name) -> dict:
        pass

    @abstractmethod
    def get_documents(self, vdb_name, collection_name) -> dict:
        pass
    
