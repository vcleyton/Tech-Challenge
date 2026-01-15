# Public Books API (Tech Challenge)

API pública para consulta de livros extraídos via web scraping do site https://books.toscrape.com/.

## Arquitetura (visão macro)
Pipeline:
1. Web Scraping → gera `data/processed/books.csv`
2. API FastAPI → carrega CSV e disponibiliza endpoints públicos
3. Consumo → cientistas de dados / serviços de recomendação / ML

## Estrutura do repositório
- `scraping/`: lógica de extração e parsing
- `scripts/`: scripts executáveis (scraping)
- `api/`: aplicação FastAPI (rotas, services)
- `data/processed/books.csv`: dataset local gerado pelo scraping

## Requisitos
- Python 3.9.x
- venv + requirements.txt

## Instalação
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt