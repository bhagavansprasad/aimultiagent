from backend.models.user_query import VectorDBQueryProcessor
from backend.utils.vdb_operations import VDBOperations 
from backend.utils.llm_utils import repharsed_queries
from backend.utils.llm_utils import prompt_llm
from collections import defaultdict
from json.decoder import JSONDecodeError

import logging
from pdbwhereami import whereami
import json
import time

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
3. Strctly follow the format of the reply in a dictionary format, like below 
# If it is a query about faqs
{
    "query":"user query",
    "reply":[
        {"faq": faq, "answer": answer},
        {"faq": faq, "answer": answer},
        ...       
    ]
}

# If it is a query with mulriple answers
{
    "query":"user query",
    "reply":[
        answer1,
        answer2,
        ...       
    ]
}
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

        print("===================")
        logging.debug("")
        logging.debug(f"Prompting LLM with prompt length :{len(prompt)}")
        logging.debug(f"prompt...")
        logging.debug(f"{prompt}")
        logging.debug("")
        print("==================")
        
        response = prompt_llm([prompt])
        logging.debug(f"Got the response from LLM of length :{len(response.text)}")
       
        return response.text 
        
    def process_query(self, query: str) -> dict:
        reply = self.basic_query(query)
        print(f"Sirijeevana: Query :{query}")
        return reply

    # {'Author': '+91 98310 27779', 'attachment': 'userdata/sirijeevana/IMG-20240917-WA0002.jpg', 'date': '2024-09-17', 'time': '10:30:00'}
    prompt_base = """### You are a strict assistant. You must only answer using the provided context.
    The context is list of rows
    Each row in the context is a csv value 'author' and 'attachment name'
    """
    prompt_context = "### Context :"
    prompt_question = "### Question: "
    prompt_answer = "### Answer:"
    prompt_rules = """
    ### Rules:
    1. Do not add any information not present in the context.
    2. With the given context compile the below statistics in a dictionary format
       msg_count: Number of messages by each Author. If the author name is empty, mark as 'unknown'
       attachments_count: Number of attachments sent by the user
       Note: Count only if the attachment is valid name is not None
       attachments: Each attachment and its author,
       meanigful_name: Name of the attachment with rephrased/normalized name, by remove spaced and unwanted words.
      {
        "Author name": {'msg_count': 'total messages count', 'attachments_count': 'attachment count'}
        "attachments": [
            "attachment name": 'Author', "meanigful_name": "repharse_name"
        ]
      }
    """
    
    def generate_prompt(self, context):
        prompt = f"""You are a data processing assistant. I have a list of CSV-like strings representing messages from users. Each string contains two columns: "Author" and "Attachment". 

        Here is the input:
        {context}

        Your task is to:
        1. Parse the data correctly, treating each string as a separate row of CSV.
        2. For each author, count:
        - The total number of messages (`msg_count`).
        - The number of attachments (`attachments_count`) that are not "None".
        3. Return the output as a JSON object, structured as below:
        4. Make sure the the output is a VALID JSON object, add missing values if needed
        {{
            "AuthorX": {{
            "msg_count": "total messages count",
            "attachments_count": "attachment count"
            }},
            "attachments": [
                {{
                    "attachmentX": "Author",
                    "meaningful_name": "rephrased_name_or_filename"
                }}
            ]
        }}
        5. For the attachments list:
        - Include each attachment along with the corresponding author.
        - Rephrase the attachment file name into a more meaningful description if possible.
        - Make sure the the output is a VALID JSON object, add missing values if needed

        Example Input:
        'Ask Nutri Foods, None'
        '+91 97313 11026, None'
        '+91 74060 00024, userdata/image.jpg'
        '+91 74060 00024, None'

        Expected JSON Output:
        {{
        "Ask Nutri Foods": {{
            "msg_count": 1,
            "attachments_count": 0
        }},
        "+91 97313 11026": {{
            "msg_count": 1,
            "attachments_count": 0
        }},
        "+91 74060 00024": {{
            "msg_count": 2,
            "attachments_count": 1
        }},
        "attachments": [
            {{
            "userdata/image.jpg": "+91 74060 00024",
            "meaningful_name": "Shared image file"
            }}
        ]
        }}


        Now, generate the consolidated report in the above JSON format based on the input data. Do not include Python code, only return the JSON result.
        """
        return prompt
    
    
    def merge_json_objects(self, json_list):
        merged_data = defaultdict(lambda: {"msg_count": 0, "attachments_count": 0})
        attachments_list = []

        for obj in json_list:
            for key, value in obj.items():
                # Merge user data (msg_count and attachments_count)
                if isinstance(value, dict) and "msg_count" in value:
                    merged_data[key]["msg_count"] += value["msg_count"]
                    merged_data[key]["attachments_count"] += value["attachments_count"]
                
                # Merge attachments list
                elif isinstance(value, list) and key == "attachments":
                    attachments_list.extend(value)

        # Deduplicate attachments based on filename
        unique_attachments = {str(att): att for att in attachments_list}.values()

        # Convert defaultdict back to a normal dict
        result = dict(merged_data)
        result["attachments"] = list(unique_attachments)

        return result
    
    def get_group_members(self, vdb_name, collection_name) -> dict:
        documents = self.siri_collection.vdb_get_stats()

        # 'metadatas': [{'Author': '', 'attachment': '', 'date': '2024-04-21', 'time': '19:00:00'},
        # Example Input:
        # 'Ask Nutri Foods, None'
        # '+91 97313 11026, None'
        # '+91 74060 00024, userdata/image.jpg'
        # userdata/sirijeevana/IMG-20240501-WA0001.jpg
        
        print(type(documents))
        chunk_size = 5000 
        
        context = []
        responses = []
        context_len = 0
        doc_len = len(documents)
        print(f"Got documents length... :{len(documents)}")
        for i, doc in enumerate(documents, 1):
            author = doc['Author'] if len(doc['Author']) > 0 else "Unknown"
            attachment = doc['attachment'] if len(doc['attachment']) > 0 else "None"
            row = f"'{author}, {attachment}',\n"
            context.append(row)
            context_len += len(row)
            # print(doc)
            # print(f"context len :{context_len}")

            if(context_len >= chunk_size):
                # print(f"{context_len}: {len(context)}")
                logging.debug(f"Processed documents :{i}/{doc_len}, context_len :{context_len}")

                prompt = self.generate_prompt(context)
                response = prompt_llm([prompt])

                text = response.text.strip('```').lstrip('json').strip()
                try:
                    responses.append(json.loads(text))
                except JSONDecodeError as err:
                    print(text)
                    print(err)
                time.sleep(5)
                context = []
                context_len = 0
                print()
            # print()

        print(f"Merging resonses len:{len(responses)}...")
        response = self.merge_json_objects(responses)

        return response
        
        logging.debug(f"Got the context of length :{len(context)}")
        logging.debug(f"Applying chunking with chunk_size :{chunk_size}")
        
        # context = context[:6000]
        # logging.debug(f"Context :{context}")
        # logging.debug(f"Context of length :{len(context)}")
        # logging.debug(f"Considering only 10k as context length...(for testing)")

        context_chunks = [context[i:i + chunk_size] for i in range(0, len(context), chunk_size)]


        for i, chunk in enumerate(context_chunks, 1):
            logging.debug(f"{i} Chunk length :{len(chunk)}...")
            prompt = self.generate_prompt(chunk)
            response = prompt_llm([prompt])
            text = response.text.strip('```').lstrip('json').strip()
            print(text)
            print()
            responses.append(json.loads(text))
            time.sleep(5)

        # Combine responses (e.g., by concatenating or summarizing)
        print(f"Merging resonses len:{len(responses)}...")
        response = self.merge_json_objects(responses)

        return response
        
    def get_stats(self, vdb_name, collection_name) -> dict:
        return {"vdb_name": vdb_name, "collection_name": collection_name, "members": ["Alice", "Bob", "Charlie"]}

    def get_documents(self, vdb_name, collection_name) -> dict:
        return {"vdb_name": vdb_name, "collection_name": collection_name, "members": ["Alice", "Bob", "Charlie"]}
    
# Buttons
    # Group members list
    # Stats
    # List of documents shared
    
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

