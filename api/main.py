from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.books import router as books_router
from api.routes.categories import router as categories_router
from api.routes.stats import router as stats_router

app = FastAPI(
    title="Public Books API",
    version="1.0.0",
    description="API de consulta de livros extraidos via web-scraping",
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(books_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(stats_router, prefix="/api/v1")