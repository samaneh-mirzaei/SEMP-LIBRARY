from typing import Optional

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel

app = FastAPI()

"""
get /books list of books -done
post /books adding books -done
get /books/{id} getting a specific book -needs to implement id
patch /books/{id} editing a specific books information -done
delete /books/{id} deleting a specific book -done
"""


class Book(BaseModel):
    title: str
    author: str
    is_available: bool = True
    published_date: Optional[str] = None


class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    is_available: Optional[bool] = None
    published_date: Optional[str] = None


books: list[Book] = []


@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(
    book: Book,
):
    books.append(book)
    return {"id": len(books) - 1, "book": book}


@app.get("/books")
def list_books():
    return [{"id": index, "book": book} for index, book in enumerate(books)]


@app.get("/books/{book_id}")
def get_book(
    book_id: int = Path(..., description="The ID of book you'd like to get"),
):
    if book_id < 0 or book_id >= len(books):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return {"id": book_id, "book": books[book_id]}


@app.patch("/books/{book_id}")
def update_book(
    *,
    book_id: int = Path(..., description="The ID of Book you'd like to edit/update"),
    updated_book: UpdateBook,
):
    if book_id < 0 or book_id >= len(books):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    update_data = updated_book.model_dump(exclude_unset=True)

    books[book_id] = books[book_id].model_copy(update=update_data)

    return {
        "message": "Book Updated",
        "ID": book_id,
        "Book": books[book_id],
    }


@app.delete("/books/{book_id}")
def delete_books(
    book_id: int = Path(..., description="The ID of Book you'd like to delete"),
):
    if book_id < 0 or book_id >= len(books):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    del books[book_id]
