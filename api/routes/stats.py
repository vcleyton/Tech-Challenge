from fastapi import APIRouter, Query
from api.services.data_store import default_data_store

router = APIRouter(tags=["stats"])


@router.get("/stats/overview")
def stats_overview():
    """
    GET /api/v1/stats/overview
    """
    store = default_data_store()
    df = store.load_books_df().copy()

    total = int(df.shape[0])
    avg_price = float(df["price"].mean()) if "price" in df.columns else None

    rating_dist = (
        df["rating"].value_counts(dropna=False).sort_index().to_dict()
        if "rating" in df.columns
        else {}
    )

    return {
        "total_books": total,
        "average_price": avg_price,
        "rating_distribution": rating_dist,
    }


@router.get("/stats/categories")
def stats_categories():
    """
    GET /api/v1/stats/overview
    """
    store = default_data_store()
    df = store.load_books_df().copy()

    if "category" not in df.columns:
        return {"categories": []}

    if "price" in df.columns:
        df["price"] = df["price"].astype(float)

    grouped = (
        df.groupby("category")
        .agg(
            books_count=("title", "count"),
            avg_price=("price", "mean"),
            min_price=("price", "min"),
            max_price=("price", "max"),
        )
        .reset_index()
        .sort_values("books_count", ascending=False)
    )

    return {"categories": grouped.to_dict(orient="records")}


@router.get("/books/top-rated")
def top_rated(limit: int = Query(default=20, ge=1, le=200)):
    """
    GET /api/v1/books/top-rated
    """
    store = default_data_store()
    df = store.load_books_df().copy()

    if "rating" not in df.columns:
        return []

    df = df.dropna(subset=["rating"]).sort_values("rating", ascending=False).head(limit)
    return df.to_dict(orient="records")


@router.get("/books/price-range")
def price_range(
    min: float = Query(default=0.0, ge=0.0),
    max: float = Query(default=999999.0, ge=0.0),
):
    """
    GET /api/v1//books/price-range
    """
    store = default_data_store()
    df = store.load_books_df().copy()

    if "price" not in df.columns:
        return []

    df["price"] = df["price"].astype(float)
    df = df[(df["price"] >= min) & (df["price"] <= max)].sort_values("price")
    return df.to_dict(orient="records")