import os
from fastapi import APIRouter
from api.services.data_store import default_data_store

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    store = default_data_store()
    return {
        "api": "ok",
        "env": os.getenv("ENV", "local"),
        "data": store.ping(),
    }