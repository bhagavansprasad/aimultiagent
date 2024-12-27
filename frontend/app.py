import streamlit as st
import requests
import json
from pdbwhereami import whereami
from slutils import display_response

# Define the FastAPI endpoints
BASE_URL = "http://localhost:8000"  # Replace with your FastAPI base URL
GET_VECTORDBS_ENDPOINT = f"{BASE_URL}/get_vectordbs"
GET_COLLECTIONS_ENDPOINT = f"{BASE_URL}/get_collections"
USER_QUERY_ENDPOINT = f"{BASE_URL}/user_query"


# Sample API endpoint (replace with actual FastAPI endpoint)
BASE_URL = "http://localhost:8000"
GET_MERGED_DATA_ENDPOINT = f"{BASE_URL}/merged_data"

# Display top 'n' users based on msg_count
def display_top_users(data, n=5):
    st.subheader(f"Top {n} Users by Message Count")

    # Sort users by msg_count in descending order
    sorted_users = sorted(
        [(user, details["msg_count"]) for user, details in data.items() if user != "attachments"],
        key=lambda x: x[1],
        reverse=True
    )

    # Display top 'n' users
    for user, msg_count in sorted_users[:n]:
        st.write(f"**{user}**: {msg_count} messages")

# List only documents (filter by 'pdf' or other keywords)
def list_documents(data):
    st.subheader("Shared Documents")

    attachments = data.get("attachments", [])
    document_list = [att for att in attachments if ".pdf" in list(att.keys())[0]]

    if document_list:
        for doc in document_list:
            for file, author in doc.items():
                if file != "meaningful_name":
                    # Extract just the file name from the full path
                    file_name = file.split("/")[-1]
                    st.write(f"📄 **{file_name}** - Shared by {author}")
    else:
        st.write("No documents found.")

def fetch_merged_data():
    response = requests.get(GET_MERGED_DATA_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data.")
        return {}

def main_app1():
    # Fetch merged data
    data = fetch_merged_data()

    if not data:
        return

    # Sidebar to select top 'n' users dynamically
    n = st.sidebar.slider("Select Top 'N' Users", min_value=1, max_value=10, value=5)

    # Display sections
    display_top_users(data, n)
    list_documents(data)


def fetch_group_members(vdb_name, collection_name):
    response = requests.get(f"{BASE_URL}/group_members", params={"vdb_name": vdb_name, "collection_name": collection_name})
    if response.status_code != 200:
        st.error("Failed to fetch group members.")
    
    n = 10
    # st.write(response.json())
    display_top_users(response.json(), n)
    list_documents(response.json())

def fetch_stats(vdb_name, collection_name):
    response = requests.get(f"{BASE_URL}/stats", params={"vdb_name": vdb_name, "collection_name": collection_name})
    # response = requests.get(f"{BASE_URL}/stats")
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error("Failed to fetch stats.")

def fetch_documents(vdb_name, collection_name):
    response = requests.get(f"{BASE_URL}/documents", params={"vdb_name": vdb_name, "collection_name": collection_name})
    # response = requests.get(f"{BASE_URL}/documents")
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error("Failed to fetch documents.")

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


def display_buttons(selected_vdb, selected_collection):
    # CSS for small buttons
    small_button_style = """
    <style>
        .small-btn {
            display: inline-block;
            padding: 3px 8px;
            font-size: 5px;
            cursor: pointer;
            border-radius: 3px;
            border: 1px solid #4CAF50;
            color: white;
            background-color: #4CAF50;
            margin-bottom: 5px;
            width: 100%;
            text-align: center;
        }
    </style>
    """
    st.sidebar.markdown(small_button_style, unsafe_allow_html=True)

    # Display buttons with smaller styling
    if st.sidebar.button("Group Members", key="btn1"):
        fetch_group_members(selected_vdb, selected_collection)

    if st.sidebar.button("Stats", key="btn2"):
        fetch_stats(selected_vdb, selected_collection)

    if st.sidebar.button("Documents", key="btn3"):
        fetch_documents(selected_vdb, selected_collection)

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
    
    st.markdown(f"<div class='small-font'>{rlist[0].strip()}</div><br>", unsafe_allow_html=True)
    
    for row in rlist[1:]:
        q, a = row.strip().split('\n')
        st.markdown(f"<div class='small-font'><b>{q.strip()}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-font'>{a.strip()}</div><br>", unsafe_allow_html=True)

def tojson(response):
    if isinstance(response['reply'], dict):
        return response
    elif isinstance(response['reply'], str):
        return json.loads(response)
    
    return None

def process_response(response):
    whereami(f"{response}")
    whereami(f"{type(response)}")
    response = response.strip('```').lstrip('json')
    
    jobj = json.loads(response)
    jobj = json.loads(jobj)
    whereami(f"{jobj}")
    whereami(f"{type(jobj)}")

    return display_response(jobj)

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
    
    display_buttons(selected_vdb, selected_collection)

    user_query = st.chat_input("What is up?")
    print(f"user_query :{user_query}")

    if user_query:
        response = post_query_to_user(selected_vdb, selected_collection, user_query)
        process_response(response)

        
def main():
    main_app()
    return

if __name__ == "__main__":
    main()

