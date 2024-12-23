from backend.models.user_query import VectorDBQueryProcessor
from backend.processors.pdf_db import pdfDBProcessor
from backend.processors.ramayana_db import RamayanaDBProcessor
from backend.processors.mahabharata_db import MahabharataDBProcessor
from backend.processors.programming_db import ProgrammingDBProcessor
from backend.processors.cholas_db import CholasDBProcessor
from backend.processors.sabarimala import SabarimalaDBProcessor
from backend.processors.sirijeevana import SirijeevanaDBProcessor
from typing import Dict

from pdbwhereami import whereami

class QueryProcessorFactory:
    _PROCESSOR_MAP: Dict[str, VectorDBQueryProcessor] = {
        "pdf-vectorDB": pdfDBProcessor,
        "ramayan-vdb": RamayanaDBProcessor,
        "mahabharata-vdb": MahabharataDBProcessor,
        "progrmmingVDB": ProgrammingDBProcessor,
        "cholas-vdb": CholasDBProcessor,
        "sabarimala-vdb": SabarimalaDBProcessor,
        "sirijeevana-vdb": SirijeevanaDBProcessor,
    }

    @staticmethod
    def get_processor(vector_db_name: str) -> VectorDBQueryProcessor:
        whereami(f"vector_db_name :{vector_db_name}")
        try:
            return QueryProcessorFactory._PROCESSOR_MAP[vector_db_name]()
        except KeyError:
            raise ValueError(f"Unknown vector DB name: {vector_db_name}")