import streamlit as st
import requests
import json
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
        # st.write("Query Results:")
        # whereami(f"response text :{response.text}")
        # st.text(response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error performing user query for '{query_text}' on {vdb_name}/{collection_name}: {e}")
        return {}

def display_qna(dreply, rlist):
    st.markdown("""
        <style>
        .small-font {
            font-size: 14px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f"**Question:** {dreply['query']}")
    
    st.markdown(f"<div class='small-font'>{rlist[0].strip()}</div>", unsafe_allow_html=True)

    
    for row in rlist[1:]:
        q, a = row.strip().split('\n')
        st.markdown(f"<div class='small-font'>{q.strip()}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-font'>{a.strip()}</div>", unsafe_allow_html=True)

def display_qna(dreply, rlist):
    st.markdown("""
        <style>
        .small-font {
            font-size: 14px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f"**Question:** {dreply['query']}")
    
    st.markdown(f"<div class='small-font'>{rlist[0].strip()}</div><br>", unsafe_allow_html=True)
    
    for row in rlist[1:]:
        q, a = row.strip().split('\n')
        st.markdown(f"<div class='small-font'><b>{q.strip()}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-font'>{a.strip()}</div><br>", unsafe_allow_html=True)
    
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

    # "common questions people have about millet consumption and provide me the answers also"
    user_query = st.chat_input("What is up?")
    print(f"user_query :{user_query}")

    if user_query:
        reply = post_query_to_user(selected_vdb, selected_collection, user_query)
        response = json.loads(reply.strip())

        reply_text = response['reply']
        rlist = reply_text.split('\n\n')
        display_qna(response, rlist)

        
def main():
    main_app()
    return

if __name__ == "__main__":
    main()
