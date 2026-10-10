from uuid import UUID

from library.schemas.book import BookRead

_books: dict[UUID, BookRead] = {}  


def get_all() -> list[BookRead]:
    return list(_books.values())


def get(book_id: UUID) -> BookRead | None:
    return _books.get(book_id)


def save(book: BookRead) -> None:
    _books[book.id] = book


def delete(book_id: UUID) -> None:
    _books.pop(book_id, None)

def clear() -> None:
    _books.clear()