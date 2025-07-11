import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch
from app import app

MOCK_GOOGLE_RESPONSE = {
    "items": [
        {
            "title": "Test result 1",
            "link": "https://example.com/1",
            "snippet": "Description 1"
        },
        {
            "title": "Test result 2",
            "link": "https://example.com/2",
            "snippet": "Description 2"
        }
    ]
}


@patch("requests.get")
def test_search_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = MOCK_GOOGLE_RESPONSE

    client = app.test_client()
    response = client.post("/search", json={"query": "test", "format": "txt"})

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/plain")
    assert "attachment" in response.headers.get("Content-Disposition", "")

    content = response.data.decode("utf-8")
    assert "Test result 1" in content
    assert "https://example.com/1" in content


def test_search_missing_query():
    client = app.test_client()
    response = client.post("/search", json={})

    assert response.status_code == 400
    assert b"Missing query" in response.data


def test_search_invalid_method():
    client = app.test_client()
    response = client.get("/search")
    assert response.status_code == 405
