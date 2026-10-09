from fastapi.testclient import TestClient
from library.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Hello, World!"


def test_create_book():
    response = client.post(
        "/books",
        json={
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "published_date": "1937-09-21",
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "The Hobbit"
    assert response.json()["id"] is not None