from uuid import UUID

from sqlalchemy.orm import Session

from library.data import book_store
from library.schemas.book import BookRead

SEED_BOOKS = [
    BookRead(
        id=UUID("11111111-1111-4111-8111-111111111111"),
        title="Dune",
        author="Frank Herbert",
        is_available=True,
        published_date="1965-08-01",
    ),
    BookRead(
        id=UUID("22222222-2222-4222-8222-222222222222"),
        title="1984",
        author="George Orwell",
        is_available=False,
        published_date="1949-06-08",
    ),
    BookRead(
        id=UUID("33333333-3333-4333-8333-333333333333"),
        title="Pride and Prejudice",
        author="Jane Austen",
        is_available=True,
        published_date="1813-01-28",
    ),
    BookRead(
        id=UUID("44444444-4444-4444-8444-444444444444"),
        title="The Hobbit",
        author="J.R.R. Tolkien",
        is_available=True,
        published_date="1937-09-21",
    ),
    BookRead(
        id=UUID("55555555-5555-4555-8555-555555555555"),
        title="Frankenstein",
        author="Mary Shelley",
        is_available=False,
    ),
]


def seed_books(db: Session) -> None:
    if book_store.get_all(db):  # don't duplicate data
        return

    for book in SEED_BOOKS:
        book_store.save(db, book)