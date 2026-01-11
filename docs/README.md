# Books Tech Challenge

## Descrição do Projeto

O **Books Tech Challenge** é uma API RESTful construída em **Python** utilizando **Flask + Flask-RESTX**, com objetivo de fornecer dados de uma coleção de livros fictícia.  

O projeto inclui:

- Scraping de livros (simulado)  
- Armazenamento em banco **SQLite**  
- Endpoints para consulta de livros, categorias e estatísticas  
- Endpoints opcionais para Machine Learning (features, dataset, predições)  
- Autenticação JWT para rotas sensíveis  
- Dashboard de monitoramento (Streamlit)  

---

## Arquitetura do Projeto

books-tech-challenge/
│
├── api/ # Código principal da API
│ ├── routes/ # Arquivos de rotas (books, categories, health, stats, auth, ml, scraping)
│ ├── database.py # Conexão e operações SQLite
│ └── app.py # Criação do app Flask + registro de namespaces
│
├── dashboard/ # Dashboard Streamlit
│ └── app.py
│
├── tests/ # Testes unitários e de integração
│ ├── test_books.py
│ ├── test_health.py
│ └── test_auth.py
│
├── docs/ # Documentação adicional
│
├── requirements.txt # Dependências do projeto
├── README.md # Este arquivo
└── pyproject.toml # Configuração do Poetry


---

## Instalação e Configuração

### Pré-requisitos

- Python 3.12+
- Git
- Poetry (ou pip)
- SQLite (já incluso no Python padrão)

### Clonar o repositório

git clone https://github.com/seu-usuario/books-tech-challenge.git
cd books-tech-challenge

### Criar ambiente virtual com Poetry

poetry install
poetry shell

### Ou usando venv + pip:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


### Configuração do Banco

O banco SQLite será criado automaticamente na primeira execução da API (arquivo books.db).

Para popular com os dados de scraping simulado via endpoint protegido:

POST /api/v1/scraping/trigger
Authorization: Bearer <ACCESS_TOKEN>


### Execução da API

Para rodar localmente:
poetry run python api/app.py

A API estará disponível em:
http://127.0.0.1:5000/api/v1/

O Swagger UI estará em:
http://127.0.0.1:5000/api/v1/


### Autenticação JWT

Para rotas protegidas (ex.: /api/v1/scraping/trigger):

POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

Resposta:

{
  "access_token": "<JWT_ACCESS_TOKEN>",
  "refresh_token": "<JWT_REFRESH_TOKEN>"
}

Para renovar o token:

POST /api/v1/auth/refresh
Authorization: Bearer <REFRESH_TOKEN>

### Endpoints da API

Books
Método	Rota	                    Descrição
GET	    /api/v1/books/	            Lista todos os livros
GET	    /api/v1/books/<id>/	        Detalhe de um livro por ID
GET	    /api/v1/books/search/	    Busca livros por título e/ou categoria
GET	    /api/v1/books/top-rated/	Lista livros melhor avaliados (limit opcional)
GET	    /api/v1/books/price-range/	Filtra livros por faixa de preço
GET	    /api/v1/books/stats/	    Estatísticas gerais da coleção

Categories
Método	Rota	                    Descrição
GET	    /api/v1/categories/	        Lista todas as categorias
GET	    /api/v1/categories/<name>/	Livros por categoria

Health
Método	Rota	                    Descrição
GET	    /api/v1/health/	            Verifica status da API e conexão com DB

Stats
Método	Rota	                    Descrição
GET	    /api/v1/stats/overview/	    Estatísticas gerais
GET	    /api/v1/stats/categories/	Estatísticas detalhadas por categoria

ML (opcional)
Método	Rota	                    Descrição
GET	    /api/v1/ml/features/	    Dados formatados para features ML
GET	    /api/v1/ml/training-data/	Dataset completo para treinamento
POST	/api/v1/ml/predictions/ 	Recebe predições de modelos ML

Scraping (protegido)
Método	Rota	                    Descrição
POST	/api/v1/scraping/trigger/	Dispara scraping (mock, protegido por JWT)

### Exemplos de chamadas

Listar livros
curl http://127.0.0.1:5000/api/v1/books/

Resposta:
[
  {
    "id": 1,
    "title": "Clean Code",
    "price": 25.99,
    "rating": 5,
    "availability": "In Stock",
    "category": "Programming",
    "image_url": "...",
    "product_url": "..."
  }
]

Buscar livros por categoria
curl http://127.0.0.1:5000/api/v1/books/search?category=Travel

Resposta:
[
  {
    "id": 5,
    "title": "Lonely Planet Guide",
    "price": 19.99,
    "rating": 4,
    "availability": "In Stock",
    "category": "Travel",
    "image_url": "...",
    "product_url": "..."
  }
]

Checagem de saúde da API
curl http://127.0.0.1:5000/api/v1/health

Resposta:
{
  "status": "ok"
}


### Testes

Para rodar todos os testes:
pytest


### Observações

As rotas estão todas documentadas via Swagger UI.

Rotas sensíveis estão protegidas por JWT (/api/v1/scraping/trigger).

O projeto está preparado para consumo de Machine Learning e integração com dashboards.

O scraping foi simulado por decisão de escopo do desafio, mantendo o foco na arquitetura de ingestão e exposição de dados. A estrutura permite fácil substituição por scraping real ou integração com pipelines externos.

## Machine Learning

Os endpoints de ML foram projetados como contrato de dados para cientistas de dados e pipelines automatizados:

/api/v1/ml/features — Features prontas para análise

/api/v1/ml/training-data — Dataset completo para treinamento

/api/v1/ml/predictions — Integração com modelos treinados

Esses endpoints permitem integração direta com notebooks, pipelines de treinamento e experimentação de modelos.


## Considerações Finais

Este projeto foi desenvolvido com foco em Engenharia de Machine Learning, indo além de uma simples API REST. Toda a arquitetura foi pensada para permitir ingestão, persistência, exposição e consumo de dados de forma estruturada e escalável.

A separação clara entre scraping, banco de dados, camada de API e endpoints voltados para Machine Learning possibilita que cientistas de dados utilizem os dados diretamente em pipelines de análise, treinamento e validação de modelos.

A adoção de Swagger garante documentação clara e reutilizável, enquanto o uso de autenticação JWT protege rotas sensíveis, alinhando o projeto com boas práticas de produção.

Apesar de utilizar SQLite por simplicidade, a arquitetura foi planejada para permitir fácil migração para bancos relacionais mais robustos, bem como integração futura com modelos de Machine Learning em produção.