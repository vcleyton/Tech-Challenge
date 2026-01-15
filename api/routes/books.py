from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from api.services.data_store import default_data_store

router = APIRouter(tags=["books"])


@router.get("/books")
def list_books():
    """
    GET /api/v1/books
    """
    store = default_data_store()
    return store.list_books()


@router.get("/books/{book_id:int}")
def get_book(book_id: int):
    """
    GET /api/v1/books/{id}
    """
    store = default_data_store()
    book = store.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro nao encontrado")
    return book


@router.get("/books/search")
def search_books(
    title: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
):
    """
    GET /api/v1/books/search?title={title}&category={category}
    """
    store = default_data_store()
    return store.search_books(title=title, category=category)