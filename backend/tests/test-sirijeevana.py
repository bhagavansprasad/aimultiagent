import os
import sys
from pdbwhereami import whereami
import logging
import json
import pytest

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_FOLDER)

from backend.processors.sirijeevana import SirijeevanaDBProcessor

test_data_basic_queries = [ 
    # {
    #     "query": "Millets",
    #     "cname": "sirijeevana",
    #     "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    # },
    # {
    #     "query": "palm jaggery",
    #     "cname": "sirijeevana",
    #     "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    # },
    # {
    #     "query": "How to prepare ambali",
    #     "cname": "sirijeevana",
    #     "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    # },
    # {
    #     "query": "How ambali can be consumed?",
    #     "cname": "sirijeevana",
    #     "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    # },
    # {
    #     "query": "recepe for ambali",
    #     "cname": "sirijeevana",
    #     "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    # },
    # {
    #     "query": "Youtube links",
    #     "cname": "sirijeevana",
    #     "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    # },
    # {
    #     "query": "Youtube links",
    #     "cname": "sirijeevana",
    #     "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    # },
    # {
    #     "query": "Messages posted by sarala",
    #     "cname": "sirijeevana",
    #     "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    # },
    # {
    #     "query": "How millets are good",
    #     "cname": "sirijeevana",
    #     "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    # },
    {
        "query": "common questions people have about millet consumption and provide me the answers also",
        "cname": "sirijeevana",
        "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    },
    # {
    #     "query": "common questions on millets and also provide me the answers",
    #     "cname": "sirijeevana",
    #     "vdb" : "/home/bhagavan/vectDBs/sirijeevana-vdb",
    # },
]
# List of videos shared in the group
@pytest.mark.parametrize("ipd", test_data_basic_queries)
def test_basic_query(ipd):
    sirij = SirijeevanaDBProcessor()
    
    original_query = ipd['query']

    print(f"Query: original_query")
    reply = sirij.basic_query(original_query)
    
    print("="*100)
    print(reply)
    print("="*100)
    

def atest_function():    
    original_query = "common questions people have about millet consumption and provide me the answers also"
    
    print(f"Query: original_query")
    sirij = SirijeevanaDBProcessor()

    reply = sirij.basic_query(original_query)

    print("="*100)
    print(reply)
    logging.debug(len(reply))
    print("="*100)

# test_basic_query()
# test_function()