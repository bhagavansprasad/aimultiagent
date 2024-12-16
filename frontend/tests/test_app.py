# frontend/tests/test_app.py

import pytest
import streamlit as st
from frontend.app import main

@pytest.fixture
def mock_query_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return {"answer": "42 is the answer to life, universe, and everything"}
    
    monkeypatch.setattr("requests.post", mock_post)

def test_user_query_ui(mock_query_response):
    # Test UI components (e.g., input field, button, etc.)
    st.write("Testing Streamlit Query")
    user_query = "What is the meaning of life?"
    
    # Assuming your frontend Streamlit app takes a user query and makes an API call
    response = mock_query_response()
    assert response["answer"] == "42 is the answer to life, universe, and everything"
