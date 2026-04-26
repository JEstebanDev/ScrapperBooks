"""Google Books API service."""
import httpx
from typing import List
from models.book import Book

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"
MAX_RESULTS = 5


async def search_books(query: str) -> List[Book]:
    """Search Google Books API and return up to 5 Book objects.

    Requests maxResults=10 to have a buffer in case some items lack a cover,
    then returns the first MAX_RESULTS books that have a cover image.
    Raises httpx errors to let the caller decide how to handle them.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GOOGLE_BOOKS_URL,
            params={"q": query, "maxResults": 10, "printType": "books"},
        )
        response.raise_for_status()
        data = response.json()

    items = data.get("items", [])
    books = []
    for item in items:
        if len(books) >= MAX_RESULTS:
            break
        info = item.get("volumeInfo", {})
        cover = info.get("imageLinks", {}).get("thumbnail", "")
        books.append(
            Book(
                title=info.get("title", ""),
                description=info.get("description", ""),
                authors=info.get("authors", []),
                cover=cover,
            )
        )
    return books
