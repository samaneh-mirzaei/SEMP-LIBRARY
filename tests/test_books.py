from fastapi.testclient import TestClient

from library import main
from library.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello, World!"


def test_create_book():
    # Clear books list before running this test for isolation
    main.books.clear()
    # Actual test
    response = client.post(
        "/books",
        json={
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "published_date": "1937-09-21",
        },
    )

    assert response.status_code == 201
    assert response.json()["book"]["title"] == "The Hobbit"
    assert response.json()["id"] == 0


def test_list_books():
    # Clear books list and add two books
    main.books.clear()
    client.post(
        "/books",
        json={
            "title": "Book A",
            "author": "Author A",
            "published_date": "2020-01-01",
        },
    )
    client.post(
        "/books",
        json={
            "title": "Book B",
            "author": "Author B",
            "published_date": "2021-02-02",
        },
    )

    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == 0
    assert data[0]["book"]["title"] == "Book A"
    assert data[1]["id"] == 1
    assert data[1]["book"]["title"] == "Book B"


def test_get_book_by_id():
    # Clear books list and add one book
    main.books.clear()
    create_response = client.post(
        "/books",
        json={
            "title": "Dune",
            "author": "Frank Herbert",
            "published_date": "1965-08-01",
        },
    )
    assert create_response.status_code == 201
    book_id = create_response.json()["id"]

    # Get the book by its id
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["book"]["title"] == "Dune"
    assert data["book"]["author"] == "Frank Herbert"
    assert data["book"]["published_date"] == "1965-08-01"
    assert data["book"]["is_available"] == True

    # Test invalid id (not found)
    response_invalid = client.get("/books/999")
    assert response_invalid.status_code == 404
    assert response_invalid.json()["detail"] == "Book not found"

    response_negative = client.get("/books/-1")
    assert response_negative.status_code == 404
    assert response_negative.json()["detail"] == "Book not found"


def test_update_book_patch():
    # Clear books list and add a book to update
    main.books.clear()
    response = client.post(
        "/books",
        json={
            "title": "Old Title",
            "author": "Old Author",
            "published_date": "2000-01-01",
        },
    )
    assert response.status_code == 201
    book_id = response.json()["id"]

    # PATCH: Change title and is_available
    patch_response = client.patch(
        f"/books/{book_id}",
        json={"title": "New Title", "is_available": False},
    )
    assert patch_response.status_code == 200
    data = patch_response.json()
    assert data["message"] == "Book Updated"
    assert data["ID"] == book_id
    assert data["Book"]["title"] == "New Title"
    assert data["Book"]["author"] == "Old Author"
    assert data["Book"]["published_date"] == "2000-01-01"
    assert data["Book"]["is_available"] is False

    # PATCH: Update with invalid id
    invalid_patch = client.patch(
        "/books/999",
        json={"title": "Doesn't Matter"},
    )
    assert invalid_patch.status_code == 404
    assert invalid_patch.json()["detail"] == "Book not found"

    negative_patch = client.patch(
        "/books/-2",
        json={"title": "Should Fail"},
    )
    assert negative_patch.status_code == 404
    assert negative_patch.json()["detail"] == "Book not found"
