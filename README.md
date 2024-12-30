- Backend (Webserver) run
<!-- uvicorn main:app --reload -->
uvicorn backend.main:app --reload

- Frontend (Streamlit) app run
<!-- streamlit run 02-slui.py -->
streamlit run frontend/app.py

<!-- Use cases -->
- test_basic_query

### TODO
#### Side bar
1. Allow users to upload new chat data
1. Allow users to upload latest chat data on existing chat
2. Allow users to choose vectorDB of their choice
#### Main Page
1. User should be able to search within search results
2. Users should be able to download documents from search results
#### Optimization
1. Impliment cache for stats
#### Features
1. Creating document's embeddings from separte process context
2. Allow search on Embedding

