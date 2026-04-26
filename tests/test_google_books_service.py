"""Tests for google_books service using unittest.mock to patch httpx."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.google_books import search_books


def _make_item(title, n):
    return {
        "volumeInfo": {
            "title": title,
            "description": f"Description {n}",
            "authors": [f"Author {n}"],
            "imageLinks": {"thumbnail": f"https://example.com/cover{n}.jpg"},
        }
    }


SAMPLE_RESPONSE = {
    "items": [_make_item(f"Book {i}", i) for i in range(1, 3)]  # 2 items
}

MANY_ITEMS_RESPONSE = {
    "items": [_make_item(f"Book {i}", i) for i in range(1, 11)]  # 10 items
}


@pytest.mark.asyncio
async def test_search_books_returns_list_of_books():
    mock_response = MagicMock()
    mock_response.json.return_value = SAMPLE_RESPONSE
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("services.google_books.httpx.AsyncClient", return_value=mock_client):
        result = await search_books("clean code")

    assert len(result) == 2
    assert result[0].title == "Clean Code"
    assert result[0].authors == ["Robert C. Martin"]
    assert result[0].cover == "https://example.com/cover.jpg"


@pytest.mark.asyncio
async def test_search_books_empty_when_no_items():
    """When API returns no items key, result should be empty list."""
    mock_response = MagicMock()
    mock_response.json.return_value = {}  # no "items" key
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("services.google_books.httpx.AsyncClient", return_value=mock_client):
        result = await search_books("xyznotfound")

    assert result == []


@pytest.mark.asyncio
async def test_search_books_handles_missing_fields():
    """Missing description, authors, imageLinks should fallback to defaults."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "items": [
            {"volumeInfo": {"title": "Bare Book"}}  # no description/authors/imageLinks
        ]
    }
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("services.google_books.httpx.AsyncClient", return_value=mock_client):
        result = await search_books("bare")

    assert len(result) == 1
    assert result[0].title == "Bare Book"
    assert result[0].description == ""
    assert result[0].authors == []
    assert result[0].cover == ""


@pytest.mark.asyncio
async def test_search_books_raises_on_httpx_error():
    """HTTPx errors should propagate (caller handles with 502)."""
    import httpx

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(side_effect=httpx.RequestError("network error"))

    with patch("services.google_books.httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(httpx.RequestError):
            await search_books("error query")
