from webserver import get_vect_dbs_list
from webserver import get_collections_list
from config import VECTOR_DBS_PATH

def test_functions():
    vdblist = get_vect_dbs_list(VECTOR_DBS_PATH)
    
    for vdb in vdblist:
        collections = get_collections_list(vdb, VECTOR_DBS_PATH)
        print(f"{vdb} : {collections}")

