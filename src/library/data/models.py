import uuid
from typing import Optional

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from library.data.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    is_available: Mapped[bool] = mapped_column(default=True)
    published_date: Mapped[Optional[str]] = mapped_column(String(32), default=None)