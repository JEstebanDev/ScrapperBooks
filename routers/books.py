"""Books search router."""
import httpx
from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.book import Book
from services.google_books import search_books

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/search", response_model=List[Book])
async def books_search(q: str = Query(..., min_length=1, description="Book title to search for")):
    if not q.strip():
        raise HTTPException(status_code=422, detail="Query parameter 'q' must not be blank.")
    try:
        return await search_books(q)
    except (httpx.RequestError, httpx.HTTPStatusError):
        raise HTTPException(status_code=502, detail="Upstream Google Books API is unavailable. Please try again later.")
