from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class BookCreate(BaseModel):
    title: str
    author: str
    published_date: str

books: list[dict] = []
next_id = 1


@app.get("/")
def home():
    return {"message": "Hello, World!"}
    

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    global next_id

    new_book = {
        "id": next_id,
        **book.model_dump(),
    }

    books.append(new_book)
    next_id += 1

    return new_book

@app.get("/books")
def list_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found",
    )