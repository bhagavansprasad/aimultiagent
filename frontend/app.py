import streamlit as st
import requests
from pdbwhereami import whereami

# Define the FastAPI endpoints
BASE_URL = "http://localhost:8000"  # Replace with your FastAPI base URL
GET_VECTORDBS_ENDPOINT = f"{BASE_URL}/get_vectordbs"
GET_COLLECTIONS_ENDPOINT = f"{BASE_URL}/get_collections"
USER_QUERY_ENDPOINT = f"{BASE_URL}/user_query"

def fetch_vectordbs():
    try:
        response = requests.get(GET_VECTORDBS_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching VectorDBs: {e}")
        return {}

def fetch_collections(vdb_name):
    try:
        response = requests.get(GET_COLLECTIONS_ENDPOINT, params={"vdb_name": vdb_name})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching collections for {vdb_name}: {e}")
        return []

def display_vectordbs(vectordbs):
    st.sidebar.title("Available VectorDBs")
    return st.sidebar.selectbox("Select a VectorDB:", vectordbs)

def display_collections(vdb_name):
    collections = fetch_collections(vdb_name)
    if not collections:
        st.warning(f"No collections found for {vdb_name}.")
        return None
    return st.sidebar.selectbox("Select a Collection:", collections)

def display_query_input(selected_vdb, selected_collection):
    query = st.text_input(f"Enter your query for {selected_vdb} - {selected_collection}:")
    return query


def post_query_to_user(vdb_name, collection_name, query_text):
    whereami(f"query_text :{query_text}")
    whereami(f"vdb_name :{vdb_name}")
    whereami(f"collection_name :{collection_name}")
    
    payload = {
        "vdb_name": vdb_name,
        "collection_name": collection_name,
        "query": query_text
    }
    
    whereami(f"payload :{payload}")
    try:
        response = requests.post(USER_QUERY_ENDPOINT, json=payload)        
        
        response.raise_for_status()
        st.write("Query Results:")
        st.text(response.text)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error performing user query for '{query_text}' on {vdb_name}/{collection_name}: {e}")
        return {}
    
def main_app():
    vectordbs_data = fetch_vectordbs()

    if not vectordbs_data:
        st.warning("No VectorDBs found.")
        return

    vectordbs = vectordbs_data.get("vectordbs", [])
    selected_vdb = display_vectordbs(vectordbs)

    if not selected_vdb:
        return
    
    selected_collection = display_collections(selected_vdb)

    user_query = st.chat_input("What is up?")
    if not user_query:
        return 0 
    
    print(f"user_query :{user_query}")

    if user_query:
        reply = post_query_to_user(selected_vdb, selected_collection, user_query)
        print(reply)
    
def main():
    main_app()
    return

if __name__ == "__main__":
    main()
