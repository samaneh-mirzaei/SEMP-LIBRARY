from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from library.data.models import Book
from library.schemas.book import BookRead


def get_all(db: Session) -> list[BookRead]:
    return [BookRead.model_validate(b) for b in db.scalars(select(Book))]


def get(db: Session, book_id: UUID) -> BookRead | None:
    book = db.get(Book, book_id)
    return BookRead.model_validate(book) if book else None


def save(db: Session, book: BookRead) -> None:
    # merge = insert if the id is new, update if it already exists
    db.merge(Book(**book.model_dump()))
    db.commit()


def delete(db: Session, book_id: UUID) -> None:
    book = db.get(Book, book_id)
    if book:
        db.delete(book)
        db.commit()