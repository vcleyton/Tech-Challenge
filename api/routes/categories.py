from fastapi import APIRouter

from api.services.data_store import default_data_store

router = APIRouter(tags=["categories"])


@router.get("/categories")
def list_categories():
    """
    GET /api/v1/categories
    """
    store = default_data_store()
    return {"categories": store.list_categories()}