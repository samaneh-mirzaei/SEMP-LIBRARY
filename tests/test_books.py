from uuid import UUID, uuid4

BOOK = {
    "title": "Dune",
    "author": "Frank Herbert",
    "published_date": "1965-08-01",
}


def create_book(client, **overrides):
    """Helper: create a book through the API and return its JSON."""
    response = client.post("/books", json={**BOOK, **overrides})
    assert response.status_code == 201
    return response.json()


# ---------- home ----------
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello, World!"


# ---------- create ----------
def test_create_book(client):
    data = create_book(client)

    UUID(data["id"])  # raises ValueError if the id isn't a valid UUID
    assert data["title"] == "Dune"
    assert data["author"] == "Frank Herbert"
    assert data["published_date"] == "1965-08-01"
    assert data["is_available"] is True  # default


def test_create_book_missing_title(client):
    response = client.post("/books", json={"author": "Nobody"})
    assert response.status_code == 422


def test_create_book_ignores_client_supplied_id(client):
    my_id = str(uuid4())
    data = create_book(client, id=my_id)
    assert data["id"] != my_id  # the server decides the id


# ---------- list ----------
def test_list_books_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []


def test_list_books(client):
    create_book(client, title="Book A")
    create_book(client, title="Book B")

    response = client.get("/books")
    assert response.status_code == 200

    titles = [book["title"] for book in response.json()]
    assert titles == ["Book A", "Book B"]


# ---------- get ----------
def test_get_book(client):
    created = create_book(client)

    response = client.get(f"/books/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_book_not_found(client):
    response = client.get(f"/books/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_get_book_invalid_id(client):
    response = client.get("/books/banana")
    assert response.status_code == 422


# ---------- update ----------
def test_update_book(client):
    created = create_book(client)

    response = client.patch(
        f"/books/{created['id']}",
        json={"title": "New Title", "is_available": False},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == created["id"]
    assert data["title"] == "New Title"
    assert data["is_available"] is False
    assert data["author"] == "Frank Herbert"          # untouched
    assert data["published_date"] == "1965-08-01"      # untouched

    # the change was actually saved
    assert client.get(f"/books/{created['id']}").json() == data


def test_update_book_not_found(client):
    response = client.patch(f"/books/{uuid4()}", json={"title": "Nope"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


# ---------- delete ----------
def test_delete_book(client):
    created = create_book(client)

    response = client.delete(f"/books/{created['id']}")
    assert response.status_code == 204

    assert client.get(f"/books/{created['id']}").status_code == 404


def test_delete_book_not_found(client):
    response = client.delete(f"/books/{uuid4()}")
    assert response.status_code == 404