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
1. Allow users to choose vectorDB of their choice
#### Main Page
1. User should be able to search within search results
1. Users should be able to download documents from search results
#### Optimization
1. Impliment cache for stats
#### Features
1. Creating document's embeddings from separte process context
1. Allow search on Embedding
1. Maintaining History
1. Search based on document names
#### Documentation
1. Creating architecture diagram
1. Sequence flow diagram for each usecase
1. REST API based documentation
#### Security/Authentication
1. Integrate OAUTH authentication
#### Special Queries
1. My postings
1. My posted documents
1. My images
1. User specific postings
1. User specific documents
1. User specific images
