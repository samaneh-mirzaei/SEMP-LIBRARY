curl.exe -X POST "http://127.0.0.1:8000/books?book=Harry%20Potter"

curl.exe http://127.0.0.1:8000/

uv run fastapi dev main.py

uv run uvicorn library.main:app --reload --app-dir src

uv run pytest

curl.exe -X POST "http://127.0.0.1:8000/books" -H "Content-Type: application/json" --data-binary '{\"title\":\"lordoftherings\"}'

.venv\Scripts\Activate.ps1

.venv\Scripts\activate.bat