from backend.models.user_query import VectorDBQueryProcessor
from backend.processors.pdf_db import pdfDBProcessor
from backend.processors.ramayana_db import RamayanaDBProcessor
from backend.processors.mahabharata_db import MahabharataDBProcessor
from backend.processors.programming_db import ProgrammingDBProcessor
from backend.processors.cholas_db import CholasDBProcessor
from backend.processors.sabarimala import SabarimalaDBProcessor

from pdbwhereami import whereami

class QueryProcessorFactory:
    
    @staticmethod
    def get_processor(vector_db_name: str) -> VectorDBQueryProcessor:
        whereami(f"vector_db_name :{vector_db_name}")
        if vector_db_name == "pdf-vectorDB":
            return pdfDBProcessor()
        elif vector_db_name == "ramayan-vdb":
            return RamayanaDBProcessor()
        elif vector_db_name == "mahabharata-vdb":
            return MahabharataDBProcessor()
        elif vector_db_name == "progrmmingVDB":
            return ProgrammingDBProcessor()
        elif vector_db_name == "cholas-vdb":
            return CholasDBProcessor()
        elif vector_db_name == "sabarimala-vdb":
            return SabarimalaDBProcessor()
        else:
            raise ValueError("Unknown vector DB name")
