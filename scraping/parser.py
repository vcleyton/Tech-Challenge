from bs4 import BeautifulSoup
import re

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def parse_book(book_soup: BeautifulSoup, category: str) -> dict:
    title = book_soup.h3.a["title"]

    price_raw = book_soup.select_one(".price_color").text
    price = float(re.sub(r"[^\d.]", "", price_raw))

    availability = (
        book_soup.select_one(".availability")
        .text.replace("\n", "")
        .strip()
    )

    rating_class = book_soup.select_one(".star-rating")["class"]
    rating = next(
        (RATING_MAP[c] for c in rating_class if c in RATING_MAP), None
    )

    image_rel_url = book_soup.img["src"].replace("../", "")
    image_url = f"https://books.toscrape.com/{image_rel_url}"

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "category": category,
        "image_url": image_url,
    }