"""Tests for the Book Pydantic model."""
from models.book import Book


def test_book_has_required_fields():
    book = Book(
        title="Clean Code",
        description="A guide to writing clean code",
        authors=["Robert C. Martin"],
        cover="https://example.com/cover.jpg",
    )
    assert book.title == "Clean Code"
    assert book.description == "A guide to writing clean code"
    assert book.authors == ["Robert C. Martin"]
    assert book.cover == "https://example.com/cover.jpg"


def test_book_defaults_to_empty_strings_and_list():
    """Fields should default to empty string / empty list when not provided."""
    book = Book(title="", description="", authors=[], cover="")
    assert book.title == ""
    assert book.description == ""
    assert book.authors == []
    assert book.cover == ""


def test_book_multiple_authors():
    book = Book(
        title="The Pragmatic Programmer",
        description="From journeyman to master",
        authors=["Andy Hunt", "Dave Thomas"],
        cover="",
    )
    assert len(book.authors) == 2
    assert "Andy Hunt" in book.authors
