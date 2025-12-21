"""
Script de Web Scraping do site https://books.toscrape.com/

Objetivo:
- Extrair todos os livros disponíveis no site
- Salvar os dados em um arquivo CSV para uso posterior na API

Campos extraídos:
- id
- title
- price
- rating
- availability
- category
- image_url
- product_url
"""

import time
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL base do site
BASE_URL = "https://books.toscrape.com/"

# Headers simples para evitar bloqueios básicos
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BookScraper/1.0)"
}


def get_soup(url: str) -> BeautifulSoup:
    """
    Faz uma requisição HTTP e retorna o BeautifulSoup da página.
    """
    response = requests.get(url, headers=HEADERS)
    response.encoding = "utf-8"
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def clean_price(price_text: str) -> float:
    """
    Remove qualquer caractere que não seja número ou ponto
    e converte para float.
    Ex: 'Â£12.29' -> 12.29
    """
    cleaned = re.sub(r"[^0-9.]", "", price_text)
    return float(cleaned)

def get_categories() -> dict:
    """
    Extrai todas as categorias disponíveis no site.

    Retorno:
    {
        "Travel": "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        ...
    }
    """
    soup = get_soup(BASE_URL)

    categories = {}

    category_list = soup.select("div.side_categories ul li ul li a")

    for category in category_list:
        name = category.text.strip()
        link = urljoin(BASE_URL, category["href"])
        categories[name] = link

    return categories


def convert_rating(rating_class: str) -> int:
    """
    Converte rating textual para número.
    Ex: "star-rating Three" -> 3
    """
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    for word, value in rating_map.items():
        if word in rating_class:
            return value

    return 0


def scrape_book_details(book_url: str, category: str, book_id: int) -> dict:
    """
    Extrai os detalhes de um único livro.
    """
    soup = get_soup(book_url)

    title = soup.find("h1").text.strip()

    price_text = soup.select_one("p.price_color").text.strip()
    price = clean_price(price_text)

    availability = soup.select_one("p.instock.availability").text.strip()

    rating_class = soup.select_one("p.star-rating")["class"]
    rating = convert_rating(" ".join(rating_class))

    image_relative_url = soup.select_one("div.item.active img")["src"]
    image_url = urljoin(book_url, image_relative_url)

    return {
        "id": book_id,
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "category": category,
        "image_url": image_url,
        "product_url": book_url
    }


def scrape_category(category_name: str, category_url: str, start_id: int) -> list:
    """
    Percorre todas as páginas de uma categoria e extrai os livros.
    """
    books = []
    page_url = category_url
    book_id = start_id

    while True:
        soup = get_soup(page_url)

        book_elements = soup.select("article.product_pod h3 a")

        for book in book_elements:
            relative_url = book["href"]
            book_url = urljoin(page_url, relative_url)

            try:
                book_data = scrape_book_details(
                    book_url=book_url,
                    category=category_name,
                    book_id=book_id
                )
                books.append(book_data)
                book_id += 1
            except Exception as e:
                print(f"Erro ao processar livro {book_url}: {e}")

            time.sleep(0.3)

        # Verifica se existe próxima página
        next_button = soup.select_one("li.next a")
        if next_button:
            page_url = urljoin(page_url, next_button["href"])
        else:
            break

    return books, book_id


def main():
    print("Iniciando scraping dos livros...")

    categories = get_categories()
    all_books = []
    current_id = 1

    for category_name, category_url in categories.items():
        print(f"Extraindo categoria: {category_name}")

        books, current_id = scrape_category(
            category_name=category_name,
            category_url=category_url,
            start_id=current_id
        )
        all_books.extend(books)

    df = pd.DataFrame(all_books)

    output_path = "data/books.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Scraping finalizado! {len(df)} livros salvos em {output_path}")


if __name__ == "__main__":
    main()


