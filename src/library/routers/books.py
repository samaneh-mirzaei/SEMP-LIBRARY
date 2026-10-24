from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from library.data.database import get_db
from library.schemas.book import BookCreate, BookRead, BookUpdate
from library.services import book_service

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db, book)


@router.get("", response_model=list[BookRead])
def list_books(db: Session = Depends(get_db)):
    return book_service.list_books(db)


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: UUID, db: Session = Depends(get_db)):
    return book_service.get_book(db, book_id)


@router.patch("/{book_id}", response_model=BookRead)
def update_book(book_id: UUID, changes: BookUpdate, db: Session = Depends(get_db)):
    return book_service.update_book(db, book_id, changes)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: UUID, db: Session = Depends(get_db)):
    book_service.delete_book(db, book_id)