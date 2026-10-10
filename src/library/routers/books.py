from uuid import UUID

from fastapi import APIRouter, status

from library.schemas.book import BookCreate, BookRead, BookUpdate
from library.services import book_service

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    return book_service.create_book(book)


@router.get("", response_model=list[BookRead])
def list_books():
    return book_service.list_books()


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: UUID):
    return book_service.get_book(book_id)


@router.patch("/{book_id}", response_model=BookRead)
def update_book(book_id: UUID, changes: BookUpdate):
    return book_service.update_book(book_id, changes)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: UUID):
    book_service.delete_book(book_id)