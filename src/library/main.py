from typing import Optional
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, HTTPException, Path, status
from pydantic import BaseModel

app = FastAPI()


class BookBase(BaseModel):
    title: str
    author: str
    is_available: bool = True
    published_date: Optional[str] = None


class BookCreate(BookBase):
    """What the client sends when creating a book."""


class BookUpdate(BaseModel):
    """What the client sends when patching. Everything is optional."""

    title: Optional[str] = None
    author: Optional[str] = None
    is_available: Optional[bool] = None
    published_date: Optional[str] = None


class BookRead(BookBase):
    """What the server returns. Includes the id."""

    id: UUID


books: dict[UUID, BookRead] = {}


def get_book_or_404(
    book_id: UUID = Path(..., description="The ID of the book"),
) -> BookRead:
    book = books.get(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.post("/books", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    new_book = BookRead(id=uuid4(), **book.model_dump())
    books[new_book.id] = new_book
    return new_book


@app.get("/books", response_model=list[BookRead])
def list_books():
    return list(books.values())


@app.get("/books/{book_id}", response_model=BookRead)
def get_book(book: BookRead = Depends(get_book_or_404)):
    return book


@app.patch("/books/{book_id}", response_model=BookRead)
def update_book(
    changes: BookUpdate,
    book: BookRead = Depends(get_book_or_404),
):
    update_data = changes.model_dump(exclude_unset=True)
    updated_book = book.model_copy(update=update_data)
    books[book.id] = updated_book
    return updated_book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book: BookRead = Depends(get_book_or_404)):
    del books[book.id]