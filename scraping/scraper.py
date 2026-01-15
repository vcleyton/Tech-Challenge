import requests
from bs4 import BeautifulSoup

from scraping.parser import parse_book

BASE_URL = "https://books.toscrape.com/"


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_categories() -> dict:
    soup = get_soup(BASE_URL)
    categories = {}

    for cat in soup.select(".side_categories ul li ul li a"):
        name = cat.text.strip()
        href = cat["href"]
        categories[name] = BASE_URL + href

    return categories


def scrape_all_books() -> list[dict]:
    books = []
    categories = get_categories()

    for category, url in categories.items():
        next_page = url

        while next_page:
            soup = get_soup(next_page)

            for book in soup.select(".product_pod"):
                books.append(parse_book(book, category))

            next_btn = soup.select_one("li.next a")
            if next_btn:
                next_page = next_page.rsplit("/", 1)[0] + "/" + next_btn["href"]
            else:
                next_page = None

    return books