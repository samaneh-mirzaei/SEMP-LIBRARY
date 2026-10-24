from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from library.config import settings
from library.data import models  # noqa: F401
from library.data.database import Base, SessionLocal, engine
from library.data.seed import seed_books
from library.exceptions import BookNotFoundError
from library.routers import books


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    if settings.seed_data:
        with SessionLocal() as db:
            seed_books(db)
    yield

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(books.router)


@app.exception_handler(BookNotFoundError)
def book_not_found_handler(request: Request, exc: BookNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "Book not found"})


@app.get("/")
def home():
    return {"message": "Hello, World!"}
