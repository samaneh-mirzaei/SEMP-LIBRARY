import pytest
from fastapi.testclient import TestClient

from library.data import book_store
from library.main import app


@pytest.fixture(autouse=True)
def clean_store():
    """Runs before and after every test so tests never affect each other."""
    book_store.clear()
    yield
    book_store.clear()


@pytest.fixture
def client():
    return TestClient(app)