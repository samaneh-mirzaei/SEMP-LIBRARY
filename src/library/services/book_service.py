from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from library.data import book_store
from library.exceptions import BookNotFoundError
from library.schemas.book import BookCreate, BookRead, BookUpdate


def create_book(db: Session, data: BookCreate) -> BookRead:
    book = BookRead(id=uuid4(), **data.model_dump())
    book_store.save(db, book)
    return book


def list_books(db: Session) -> list[BookRead]:
    return book_store.get_all(db)


def get_book(db: Session, book_id: UUID) -> BookRead:
    book = book_store.get(db, book_id)
    if book is None:
        raise BookNotFoundError(book_id)
    return book


def update_book(db: Session, book_id: UUID, changes: BookUpdate) -> BookRead:
    book = get_book(db, book_id)  # raises if missing
    updated = book.model_copy(update=changes.model_dump(exclude_unset=True))
    book_store.save(db, updated)
    return updated


def delete_book(db: Session, book_id: UUID) -> None:
    get_book(db, book_id)  # raises if missing
    book_store.delete(db, book_id)