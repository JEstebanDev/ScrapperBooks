"""Tests for GET /books/search router."""
import pytest
import httpx
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import app
from models.book import Book

client = TestClient(app)

SAMPLE_BOOKS = [
    Book(
        title="Clean Code",
        description="A guide to writing clean code",
        authors=["Robert C. Martin"],
        cover="https://example.com/cover.jpg",
    )
]


def test_search_books_200_returns_books():
    with patch(
        "routers.books.search_books", new_callable=AsyncMock
    ) as mock_search:
        mock_search.return_value = SAMPLE_BOOKS
        response = client.get("/books/search?q=clean+code")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Clean Code"
    assert data[0]["authors"] == ["Robert C. Martin"]
    assert data[0]["cover"] == "https://example.com/cover.jpg"


def test_search_books_200_empty_list_when_no_results():
    with patch(
        "routers.books.search_books", new_callable=AsyncMock
    ) as mock_search:
        mock_search.return_value = []
        response = client.get("/books/search?q=xyznotfoundatall")

    assert response.status_code == 200
    assert response.json() == []


def test_search_books_422_when_q_missing():
    """Missing required query param `q` should return 422 (FastAPI validation)."""
    response = client.get("/books/search")
    assert response.status_code == 422


def test_search_books_502_on_google_api_failure():
    """When Google Books API fails, return 502."""
    with patch(
        "routers.books.search_books", new_callable=AsyncMock
    ) as mock_search:
        mock_search.side_effect = httpx.RequestError("network error")
        response = client.get("/books/search?q=clean+code")

    assert response.status_code == 502
    assert "upstream" in response.json()["detail"].lower() or response.status_code == 502
