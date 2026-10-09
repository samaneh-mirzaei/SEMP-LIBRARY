from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Book(BaseModel):
    title: str
    author: str
    published_date: str
    description: str = None
    available: bool = True
    id: int = None  
    created_at: str = None
    updated_at: str = None
    deleted_at: str = None
    borrowed_by: str = None
    borrowed_date: str = None
    returned_date: str = None

books = []


@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/books")
def list_books(limit: int = 10):
    return {"message": "Books", "books": books[:limit]}

@app.get("/books/{book_id}")
def get_book(book_id: int) -> Book:
    if book_id < 0 or book_id >= len(books):
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return {"message": "Book", "book": books[book_id]}

@app.post("/books")
def create_book(book: Book):
    books.append(book.model_dump())
    return books

