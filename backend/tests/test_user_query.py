# backend/tests/test_user_query.py

from fastapi.testclient import TestClient
from backend.main import app  # FastAPI app instance

client = TestClient(app)

def test_user_query():
    payload = {
        "query": "What is the meaning of life?",
        "vector_db_name": "chroma",
        "collection": "default"
    }
    response = client.post("/user_query", json=payload)
    assert response.status_code == 200
    assert "answer" in response.json()
