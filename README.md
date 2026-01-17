# 📚 Tech Challenge - Books API com Machine Learning

A **Tech Challenge Books API** é uma api completa e escalável para gerenciamento livros. Construída com Flask e integrada com tecnologias modernas, esta API oferece funcionalidades avançadas de machine learning para predição de preços, gerenciamento seguro de dados com autenticação JWT e coleta de dados automatizada via web scraping.

Ideal para plataformas de e-commerce de livros, bibliotecas digitais e sistemas de análise de dados bibliográficos, esta API combina performance, segurança e escalabilidade em uma solução pronta para produção.

## 📑 Índice de Navegação

- [Objetivos do Projeto](#-objetivos-do-projeto)
- [Links Importantes](#-links-importantes)
- [Arquitetura do Projeto](#️-arquitetura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Autenticação JWT](#-autenticação-jwt)
- [Endpoints da API](#-endpoints-da-api)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Machine Learning](#-machine-learning---detalhes-técnicos)
- [Ferramentas e Tecnologias](#️-ferramentas-e-tecnologias)
- [Segurança](#-segurança)
- [Escalabilidade](#-escalabilidade)
- [Variáveis de ambiente](#-variáveis-de-ambiente)
- [Contribuindo](#-contribuindo)
- [Autores](#-autores)
- [Contato](#-contato)

## 🎯 Objetivos do Projeto

- **💾 Consulta e Busca Avançada de Livros**: Acesso completo aos dados de livros com filtros por preço, categoria, avaliação e título.
- **🤖 Predição Inteligente de Preços**: Modelo de Machine Learning (RandomForest Regressor) treinado para prever preços baseado em características do livro (categoria, rating e estoque)
- **🔐 Autenticação e Autorização Segura**: Implementação de JWT (JSON Web Tokens) para proteger endpoints sensíveis como treinamento de modelos e garantir acesso autorizado
- **🕷️ Web Scraping Automatizado**: Integração com Scrapy para coleta automatizada de dados de livros de fontes externas, mantendo o catálogo sempre atualizado
- **📊 Análise Estatística Robusta**: Endpoints para gerar insights sobre o catálogo, incluindo preço médio, distribuição de ratings e análise por categoria
- **⚙️ Arquitetura Escalável e Modular**: Design em camadas (Routes → Services → Repository → Data) para suportar crescimento futuro e fácil integração de novos modelos de ML


## 🔗 Links Importantes

- **Deploy**: <https://tech-challenge-0upc.onrender.com>
- **Vídeo Demonstração**: [Link do Vídeo] *(a ser preenchido)*
- **Documentação Swagger**: Disponível em `/apidocs` quando a aplicação estiver rodando

## 🏗️ Arquitetura do Projeto

### Diagrama Visual da Arquitetura

![Arquitetura do Sistema - Tech Challenge](assets/DiagramaArquitetural.jpeg)

### Pipeline do Projeto

```
Ingestão (Web Scraping e dados de registro de usuários)
    ↓
Armazenamento (Dados são armazenados em banco de dados SQLite)
    ↓
Processamento (As interações com os bancos de dados são feitas na camada de repositórios, a camada de serviços é onde as informações são processadas, tratadas e validadas)
    ↓
API (Endpoints REST na camada de rotas)
    ↓
Consumo (Clientes da API)
```

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/vcleyton/Tech-Challenge.git
cd "Tech-Challenge"
```

### 2. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do Banco de Dados
DATABASE_URI=sqlite:///user.db

# Chaves de Segurança
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Configurações de esquema do swagger (http, https)
SWAGGER_SCHEMES=http
```

### 5. Gerar Chaves de Segurança

```bash
python generate_keys.py
```

### 6. Executar Web Scraper para Popular o Banco de Dados

Antes de iniciar a API, é necessário executar o scraper do Scrapy para coletar os dados dos livros e criar o banco de dados `book.db`.

#### 6.1 Navegar para a pasta do Scraper

```bash
cd src/scraper
```

#### 6.2 Executar o Spider de Livros

```bash
# Windows
scrapy crawl books

# macOS/Linux
python -m scrapy crawl books
```

**O que acontece durante o scraping:**

1. **Coleta de Dados**: O spider acessa [books.toscrape.com](https://books.toscrape.com) e extrai informações de todos os livros
2. **Extração de Informações**: Para cada livro, coleta:
   - Título
   - Preço
   - Quantidade em estoque
   - Avaliação (rating)
   - Categoria
   - URL da imagem

3. **Pipeline de Processamento**: Os dados passam pelo pipeline que:
   - Valida as informações
   - Insere os dados no banco SQLite `instance/books.db`

4. **Tempo Estimado**: O scraping leva aproximadamente 10-15 minutos (com delay de 1 segundo entre requisições para respeitar o servidor)

#### 6.3 Esperado Durante a Execução

```
2025-01-13 10:30:45 [scrapy.utils.log] INFO: Scrapy 2.13.3 started in debug mode
2025-01-13 10:30:45 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023
2025-01-13 10:30:46 [scrapy.middleware.httpcache] INFO: Using httpcache storage in /path/to/project/.scrapy/httpcache
2025-01-13 10:30:47 [BookToScrape.pipelines] INFO: Book added: 'A Light in the Attic'
2025-01-13 10:30:48 [BookToScrape.pipelines] INFO: Book added: 'Tango with Django'
...
2025-01-13 10:45:12 [BookToScrape.spiders.books] INFO: Closed spider (finished)
```

#### 6.4 Verificar se os Dados Foram Salvos

Após o scraping terminar com sucesso, você verá o arquivo `books.db` na pasta `instance/`:

```bash
# Voltar para a raiz do projeto
cd ../..

# Verificar se o arquivo foi criado
dir instance/  # Windows
ls instance/   # macOS/Linux
```

Você deve ver:
```
instance/
└── books.db          # ✅ Banco de dados de livros (recém-criado)
```

#### 6.5 Solucionar Problemas Comuns

**Erro: "Spider not found"**
```bash
# Certifique-se de estar na pasta src/scraper
cd src/scraper
scrapy crawl books
```

**Erro: "Connection refused" ou "Timeout"**
```bash
# Verificar conexão com internet e tentar novamente
# O site pode estar temporariamente indisponível
```

**Scraping muito lento**
- Normal! O delay está configurado em 1 segundo entre requisições para respeitar o servidor
- Você pode ajustar em `src/scraper/BookToScrape/settings.py` se necessário

### 7. Inicializar a Aplicação

```bash
python app.py
```

A aplicação criará automaticamente as tabelas necessárias para usuários no banco SQLite `instance/user.db`.

## 📁 Estrutura do Projeto

```
Tech Challenge/
├── app.py                    # Ponto de entrada da aplicação
├── generate_keys.py          # Script para gerar chaves de segurança
├── requirements.txt          # Dependências Python
├── README.md                 # Este arquivo
├── .env                      # Variáveis de ambiente (não versionado)
│
├── src/
│   ├── __init__.py          # Factory function create_app()
│   ├── extensions.py        # Extensões Flask (SQLAlchemy, JWT)
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py        # Configurações da aplicação
│   │
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── books.py         # Modelo Book
│   │   └── user.py          # Modelo User
│   │
│   ├── repository/          # Camada de acesso a dados
│   │   ├── __init__.py
│   │   ├── books_repository.py
│   │   └── user_repository.py
│   │
│   ├── routes/              # Blueprints com rotas
│   │   ├── __init__.py
│   │   ├── auth.py          # Autenticação
│   │   ├── books.py         # Gerenciamento de livros
│   │   ├── ml.py            # Machine Learning
│   │   ├── stats.py         # Estatísticas
│   │   └── health.py        # Health check
│   │
│   ├── services/            # Lógica de negócios
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── books_service.py
│   │   └── ml_service.py
│   │
│   ├── scraper/             # Web scraper com Scrapy
│   │   ├── scrapy.cfg
│   │   └── BookToScrape/
│   │       ├── __init__.py
│   │       ├── items.py
│   │       ├── pipelines.py
│   │       ├── settings.py
│   │       └── spiders/
│   │           ├── __init__.py
│   │           └── books.py
│   │
│   └── utils/               # Utilitários
│       ├── __init__.py
│       ├── exceptions.py    # Exceções customizadas
│       └── validators.py    # Validadores
│
├── assets/                       # Pasta de imagens
│   ├── DiagramaArquitetural.jpeg # Imagem da arquitetura do projeto
│
└── instance/                # Arquivos de instância (não versionados)
    ├── user.db              # Banco de dados SQLite com dados do usuário
    ├── books.db             # Banco de dados SQLite com dados de livros
    ├── ml_model.joblib      # Modelo ML treinado
    ├── encoder.joblib       # Encoder OneHot
    └── feature_order.joblib # Ordem das features
```

## 🔐 Autenticação JWT

A API utiliza **JWT (JSON Web Tokens)** para autenticação segura de endpoints sensíveis.

### Como Funciona
1. O usuário faz login enviando credenciais (`username` e `password`)
2. A API retorna um token JWT com validade de **30 minutos**
3. O cliente inclui o token no header `Authorization: Bearer <token>` para acessar endpoints protegidos
4. A API valida o token em cada requisição

### Bearer Token Header
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Endpoints Protegidos
- `POST /ml/train-model` - Requer autenticação para treinar modelo

### Token Expirado
Se o token expirar (após 30 minutos), faça login novamente para obter um novo token.

## 📚 Endpoints da API

### Base URL
```
http://localhost:5000
```

### 🔐 Autenticação - `/auth`

#### Registrar Novo Usuário
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "senha123"
}
```

**Response (201 Created):**
```json
{
  "message": "Usuário registrado com sucesso"
}
```

**Errors:**
- `400 Bad Request`: Username ou senha não fornecidos, ou formato inválido
- `409 Conflict`: Usuário já existe
- `422 Unprocessable Entity`: Dados inválidos ou não atendendo aos requisitos

---

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "senha123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Errors:**
- `400 Bad Request`: Username ou senha não fornecidos, ou formato inválido
- `401 Unauthorized`: Username ou password inválidos
- `500 Internal Server Error`: Erro ao fazer login

### 📚 Livros - `/books`

#### Listar Todos os Livros
```http
GET /books
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "A Light in the Attic",
    "category": "Poetry",
    "price": "51.77",
    "rating": "3",
    "stock": 22,
    "image_url": "http://example.com/image.jpg"
  },
  {
    "id": 2,
    "title": "Tango with Django",
    "category": "Programming",
    "price": "23.10",
    "rating": "3",
    "stock": 0,
    "image_url": "http://example.com/image2.jpg"
  }
]
```

**Errors:**
- `500 Internal Server Error`: Erro ao buscar livros

---

#### Obter Detalhes de um Livro
```http
GET /books/{id}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "A Light in the Attic",
  "category": "Poetry",
  "price": "51.77",
  "rating": "3",
  "stock": 22,
  "image_url": "http://example.com/image.jpg"
}
```

**Errors:**
- `400 Bad Request`: ID inválido (deve ser um inteiro positivo)
- `404 Not Found`: Livro com esse ID não encontrado
- `500 Internal Server Error`: Erro ao buscar livro

---

#### Buscar Livros com Filtros
```http
GET /books/search?title=harry&min_price=10&max_price=30&category=Fiction
```

**Parâmetros Query (todos opcionais):**
- `title`: Título ou parte do título a buscar
- `min_price`: Preço mínimo do livro
- `max_price`: Preço máximo do livro
- `category`: Categoria do livro
- `min_rating`: Avaliação mínima (0-5)
- `max_rating`: Avaliação máxima (0-5)

**Response (200 OK):**
```json
[
  {
    "id": 3,
    "title": "Harry Potter and the Philosopher's Stone",
    "category": "Fiction",
    "price": "15.50",
    "rating": "5",
    "stock": 50,
    "image_url": "http://example.com/image.jpg"
  }
]
```

Retorna lista vazia se nenhum livro atender aos critérios.

**Errors:**
- `400 Bad Request`: Parâmetros de filtro inválidos (preços devem ser números, ratings devem estar entre 0-5, min_price não pode ser maior que max_price, min_rating não pode ser maior que max_rating)
- `500 Internal Server Error`: Erro ao buscar livros

---

#### Obter Todas as Categorias
```http
GET /books/categories
```

**Response (200 OK):**
```json
[
  "Poetry",
  "Programming",
  "Fiction",
  "Mystery",
  "Philosophy",
  "Romance",
  "Travel"
]
```

**Errors:**
- `500 Internal Server Error`: Erro ao buscar categorias

### 📊 Estatísticas - `/stats`

#### Visão Geral de Estatísticas
```http
GET /stats/overview
```

**Response (200 OK):**
```json
{
  "total_books": 1000,
  "average_price": 28.45,
  "distribution_rating": [
    {
      "rating": "3",
      "count": 250
    },
    {
      "rating": "4",
      "count": 350
    },
    {
      "rating": "5",
      "count": 400
    }
  ]
}
```

**Errors:**
- `500 Internal Server Error`: Erro ao buscar estatísticas

---

#### Estatísticas por Categoria
```http
GET /stats/categories
```

**Response (200 OK):**
```json
[
  {
    "category": "Fiction",
    "total_books": 250,
    "average_price": 25.50
  },
  {
    "category": "Poetry",
    "total_books": 150,
    "average_price": 30.20
  },
  {
    "category": "Programming",
    "total_books": 120,
    "average_price": 45.80
  }
]
```

**Errors:**
- `500 Internal Server Error`: Erro ao buscar estatísticas

### 🤖 Machine Learning - `/ml`

#### Obter Features Disponíveis
```http
GET /ml/features
```

**Response (200 OK):**
```json
[
  {
    "stock": 22,
    "rating": 3,
    "category_Fiction": 0.0,
    "category_Poetry": 1.0,
    "category_Programming": 0.0,
    "category_Mystery": 0.0
  }
]
```

**Errors:**
- `500 Internal Server Error`: Erro ao obter features

---

#### Obter Dados de Treinamento
```http
GET /ml/training-data
```

**Response (200 OK):**
```json
[
  {
    "stock": 22,
    "rating": 3,
    "price": 51.77,
    "category_Fiction": 0.0,
    "category_Poetry": 1.0,
    "category_Programming": 0.0
  }
]
```

**Errors:**
- `500 Internal Server Error`: Erro ao obter dados de treinamento

---

#### Treinar Modelo (Requer Autenticação)
```http
POST /ml/train-model
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Modelo treinado com sucesso"
}
```

**Errors:**
- `401 Unauthorized`: Token não fornecido ou inválido
- `500 Internal Server Error`: Erro ao treinar modelo (dados insuficientes, modelo já treinado, erro na codificação)

---

#### Fazer Predição de Preço
```http
POST /ml/predict
Content-Type: application/json

{
  "category": "Fiction",
  "stock": 10,
  "rating": 4
}
```

**Response (200 OK):**
```json
{
  "predicted_price": 25.45
}
```

**Errors:**
- `400 Bad Request`: Parâmetros obrigatórios ausentes (category, stock, rating), valores inválidos (stock deve ser inteiro não negativo, rating deve estar entre 0-5, category deve ser string não vazia), ou categoria não existe
- `500 Internal Server Error`: Erro ao fazer predição, modelo não treinado, ou erro na codificação

### 🏥 Health Check - `/health`

#### Verificar Status da API
```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "OK"
}
```

Para status completo e detalhado, use `GET /health/status`:

```json
{
  "status": "OK",
  "version": "1.0.0",
  "timestamp": "2025-01-17T10:30:45Z",
  "uptime_seconds": 3600,
  "components": {
    "user_database": {"status": "OK", "tables": 2},
    "books_database": {"status": "OK", "tables": 1},
    "jwt": {"status": "OK"},
    "services": {"status": "OK"}
  }
}
```

**Errors:**
- `200 OK`: Sempre retorna status 200 (mesmo em caso de degradação, status será "DEGRADED")

## 💻 Exemplos de Uso

### Com CURL

```bash
# Registrar um novo usuário
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "senha123"}'

# Fazer login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "senha123"}'

# Listar todos os livros
curl http://localhost:5000/books

# Obter detalhes de um livro
curl http://localhost:5000/books/1

# Buscar livros com filtros
curl "http://localhost:5000/books/search?title=harry&min_price=10&max_price=30"

# Fazer predição de preço
curl -X POST http://localhost:5000/ml/predict \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Fiction",
    "stock": 10,
    "rating": 4
  }'
```

### Com Python

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# 1. Registrar usuário
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={"username": "john", "password": "pass123"}
)
print(response.json())

# 2. Fazer login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "john", "password": "pass123"}
)
token = response.json()["access_token"]

# 3. Treinar modelo (com autenticação)
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/ml/train-model",
    headers=headers
)
print(response.json())

# 4. Fazer predição
response = requests.post(
    f"{BASE_URL}/ml/predict",
    json={"category": "Fiction", "stock": 10, "rating": 4}
)
print(response.json())

# 5. Listar todos os livros
response = requests.get(f"{BASE_URL}/books")
print(response.json())

# 6. Obter estatísticas
response = requests.get(f"{BASE_URL}/stats/overview")
print(response.json())
```

## 🤖 Machine Learning - Detalhes Técnicos

### Modelo
- **Algoritmo**: RandomForest Regressor
- **Features**: Stock, Rating, Category (one-hot encoded)
- **Target**: Preço do livro

### Pipeline de ML
1. **Coleta de Dados**: Dados são extraídos do banco SQLite via `/ml/training-data`
2. **Preparação**: Features são codificadas (one-hot encoding para categorias)
3. **Treinamento**: RandomForest é treinado com os dados preparados
4. **Persistência**: Modelo é salvo em `instance/ml_model.joblib`
5. **Predição**: Novos dados são processados e predições são geradas

### Melhorias Futuras para ML
- Implementação de múltiplos modelos (Gradient Boosting, XGBoost)
- Cross-validation para validação robusta
- Hyperparameter tuning automático
- API para A/B testing de modelos
- Versionamento de modelos
- Monitoramento de model drift

## 🛠️ Ferramentas e Tecnologias

### Backend
- **Flask**: Framework web minimalista e flexível
- **Flask-SQLAlchemy**: ORM (Object Relational Mapping) para gerenciamento de dados
- **Flask-JWT-Extended**: Autenticação com JWT
- **Flask-RESTx**: Framework REST com documentação automática

### Machine Learning
- **scikit-learn**: Biblioteca de ML com RandomForest
- **joblib**: Serialização de modelos ML e transformadores
- **pandas**: Manipulação de dados

### Web Scraping
- **Scrapy**: Framework robusto para web scraping

### Infraestrutura
- **SQLite**: Banco de dados leve e portável
- **Python 3.8+**: Linguagem de programação

### Documentação
- **Flasgger**: Documentação automática Swagger/OpenAPI

## 🔐 Segurança

- **Autenticação JWT**: Tokens com expiração de 30 minutos
- **Validação de Entrada**: Todos os inputs são validados
- **Tratamento de Erros**: Respostas padronizadas com códigos HTTP apropriados
- **Variáveis de Ambiente**: Chaves sensíveis não são versionadas

## 📈 Escalabilidade

### Arquitetura Pensada para Crescimento

1. **Camadas Separadas**: Fácil substituição de componentes
2. **Microserviços Prontos**: Serviços podem ser isolados
3. **Banco de Dados**: Suporta migração SQLite → PostgreSQL
4. **Cache**: Pronto para Redis
5. **Queue**: Suporta integração com Celery para tarefas assíncronas

### Próximos Passos
- [ ] Migrar para PostgreSQL
- [ ] Implementar Redis para cache
- [ ] Adicionar Celery para tarefas assíncronas
- [ ] Containerizar com Docker
- [ ] Deploy em Kubernetes
- [ ] Adicionar CI/CD com GitHub Actions

## 📝 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_URI` | Connection string do banco de dados | `sqlite:///user.db` |
| `SECRET_KEY` | Chave para sessões Flask | - |
| `JWT_SECRET_KEY` | Chave para assinar JWT | - |
| `SWAGGER_SCHEMES` | Define o protocolo de transferência da api | `http ou https` |

## 🤝 Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## 👥 Autores

- Cleyton Barroca
- Jonatas Locateli
- Tiago Faustino
- Ralph Vieira 
- Andrea Oliveira

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Última atualização**: Janeiro 2026