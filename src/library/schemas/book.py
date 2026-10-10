from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    is_available: bool = True
    published_date: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    is_available: Optional[bool] = None
    published_date: Optional[str] = None


class BookRead(BookBase):
    id: UUID