import pandas as pd

from scraping.scraper import scrape_all_books


def main():
    books = scrape_all_books()
    df = pd.DataFrame(books)

    output_path = "data/processed/books.csv"
    df.to_csv(output_path, index=False)

    print(f"OK! Livros obtidos: {len(df)} ")


if __name__ == "__main__":
    main()