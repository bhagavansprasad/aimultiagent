from backend.models.user_query import VectorDBQueryProcessor
from backend.utils.vdb_operations import VDBOperations 
from backend.utils.llm_utils import repharsed_queries
from backend.utils.llm_utils import prompt_llm

import logging
from pdbwhereami import whereami

# Q. List of videos shared in the group?
# Parse youtube links
prompt_base = "### You are a strict assistant. You must only answer using the provided context."
prompt_context = "### Context:"
prompt_question = "### Question: "
prompt_answer = "### Answer:"
prompt_rules = """
### Rules:
1. Do not add any information not present in the context.
2. If the answer is not found in the context, reply with "The information is not available in the provided context."
"""
from backend.config import Config
    
class SirijeevanaDBProcessor(VectorDBQueryProcessor):
    # Sirijeevana collection obj
    siri_collection = None

    # VectorDB     
    vdbs_path = Config.VECTOR_DBS_PATH
    vdb_name = vdbs_path + Config.SIRIJEEVANA_VECTOR_DB_NAME
    cname = Config.SRIRIJEEVANA_COLLECTION_NAME
    
    def __init__(self):
        logging.debug(f"vdb_name :{self.vdb_name}")
        logging.debug(f"cname    :{self.cname}")
        self.siri_collection = VDBOperations(self.vdb_name, self.cname)
        
    # def basic_query(self, original_query: str, cname: str, vdb_name: str) -> str:
    def basic_query(self, original_query: str) -> str:
        context = ""
       
        queries = repharsed_queries(original_query)
        logging.debug(f"Rephrased queries count :{len(queries)}")
        logging.debug(f"{queries}")
        
        for query in queries:
            context += self.siri_collection.vdb_get_documents_by_query(query)

        logging.debug(f"Got the context of length :{len(context)}")

        prompt = "\n\n".join([prompt_base, prompt_context, context, prompt_question, original_query, prompt_rules, prompt_answer])

        logging.debug(f"Prompting LLM with prompt length :{len(prompt)}")
        
        response = prompt_llm([prompt])
        logging.debug(f"Got the response from LLM of length :{len(response.text)}")
       
        return response.text 
        
    def process_query(self, query: str, collection: str, vdb_name: str) -> dict:
        reply = self.basic_query(query, collection, vdb_name)
        print(f"{vdb_name}->{collection}: Query :{query}")
        return {"answer": reply}
    
    
# Q. Share me cough protocol
# The answer will not have any link with question
# Even the user is replied to the question but, the link is not maintained in exported chat
# We may need to search probable answer in next 24 hours time frame
# Reply to this question is refer the 'lungs section' in the protocol document
# We may need to process pdf file's text and images

# Q. How many questions that I have posted
# Filter messages based on user and filter out questions
# We may need to process complete collection

# Q. Build FAQs
# Filter out all Questions and probable answers for each

# Q. Share me links
# Filter out all links shared in the group

# Q. Sirijeevana session announcements
# List of sessions conducted and their dates, locations

# Q. Links to prepare for ambali
# 1. Search links and share if it is related with Ambali
# 2. Seach questions that are posted for Ambali preparation, search answers to those?

