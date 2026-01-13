# 📚 Tech Challenge - Book API com Machine Learning

Uma API robusta para gerenciamento de livros com integração de Machine Learning para predição de preços, autenticação segura e análise estatística de dados.

## 🎯 Objetivos do Projeto

- **Gerenciamento de Livros**: API REST completa para CRUD de livros com informações detalhadas
- **Predição de Preços com ML**: Utilizar Machine Learning (RandomForest Regressor) para prever preços baseado em características
- **Autenticação Segura**: Implementar JWT para proteger endpoints sensíveis
- **Análise de Dados**: Fornecer estatísticas e insights sobre a base de dados de livros
- **Web Scraping**: Integração com Scrapy para coleta automatizada de dados de livros
- **Arquitetura Escalável**: Design pensado para suportar crescimento futuro e integração com múltiplos modelos de ML

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE (Web/Mobile)                     │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CAMADA DE API (Flask)                       │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │Auth Routes │ │Book Routes │ │Stats Routes│ │ML Routes   │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
└────────────┬─────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADA DE SERVIÇOS                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│  │AuthService   │ │BooksService  │ │MLService     │             │
│  └──────────────┘ └──────────────┘ └──────────────┘             │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADA DE REPOSITÓRIO                         │
│  ┌──────────────┐ ┌──────────────┐                              │
│  │UserRepository│ │BooksRepository                              │
│  └──────────────┘ └──────────────┘                              │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CAMADA DE DADOS                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│  │SQLite (Users)│ │SQLite (Books)│ │ML Models (   │             │
│  │              │ │              │ │ joblib files)│             │
│  └──────────────┘ └──────────────┘ └──────────────┘             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    WEB SCRAPER (Scrapy)                          │
│  Ingestão de dados → Processamento → Armazenamento em DB        │
└─────────────────────────────────────────────────────────────────┘
```

### Pipeline de Dados

```
Ingestão (Web Scraper)
    ↓
Processamento (Validação & Transformação)
    ↓
Armazenamento (SQLite)
    ↓
API (Endpoints REST)
    ↓
Consumo (Clientes da API)
    ↓
Machine Learning (Treinamento & Predição)
```

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- SQLite3
- Git

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone <seu-repositorio>
cd "Tech Challenge"
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
```

### 5. Gerar Chaves de Segurança

```bash
python generate_keys.py
```

### 6. Executar Web Scraper para Popular o Banco de Dados (IMPORTANTE)

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
   - Insere os dados no banco SQLite `instance/book.db`

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

Após o scraping terminar com sucesso, você verá o arquivo `book.db` na pasta `instance/`:

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
├── book.db          # ✅ Banco de dados de livros (recém-criado)
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

### 7. Inicializar o Banco de Dados de Usuários

```bash
python app.py
```

A aplicação criará automaticamente as tabelas necessárias para usuários no banco SQLite `instance/user.db`.

## 📖 Documentação das Rotas da API

### Base URL
```
http://localhost:5000
```

### Autenticação (JWT)

A API utiliza JWT Bearer tokens. Para acessar endpoints protegidos, inclua o token no header:

```
Authorization: Bearer <seu-jwt-token>
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
- `400 Bad Request`: Dados inválidos
- `409 Conflict`: Username já existe

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
- `400 Bad Request`: Credenciais inválidas
- `401 Unauthorized`: Username ou senha incorretos

### 📚 Livros - `/books`

#### Listar Todos os Livros
```http
GET /books/
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "A Great Book",
    "price": "19.99",
    "stock": 10,
    "rating": "4.5",
    "category": "Fiction",
    "image_url": "https://example.com/image.jpg"
  },
  {
    "id": 2,
    "title": "Another Book",
    "price": "24.99",
    "stock": 5,
    "rating": "4.2",
    "category": "Mystery",
    "image_url": "https://example.com/image2.jpg"
  }
]
```

#### Obter Detalhes de um Livro
```http
GET /books/{id}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "A Great Book",
  "description": "A wonderful story...",
  "price": "19.99",
  "stock": 10,
  "rating": "4.5",
  "category": "Fiction",
  "image_url": "https://example.com/image.jpg"
}
```

**Errors:**
- `404 Not Found`: Livro não encontrado

#### Buscar Livros com Filtros
```http
GET /books/search?title=harrypotter&min_price=10&max_price=30&category=Fiction&min_rating=3&max_rating=5
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
    "id": 5,
    "title": "Harry Potter and the Philosopher's Stone",
    "price": "15.99",
    "stock": 8,
    "rating": "4.8",
    "category": "Fiction",
    "image_url": "https://example.com/harry.jpg"
  }
]
```

**Errors:**
- `400 Bad Request`: Parâmetros de busca inválidos

#### Obter Todas as Categorias
```http
GET /books/categories
```

**Response (200 OK):**
```json
[
  "Fiction",
  "Mystery",
  "Science Fiction",
  "Romance",
  "Biography"
]
```

### 📊 Estatísticas - `/stats`

#### Visão Geral de Estatísticas
```http
GET /stats/overview
```

**Response (200 OK):**
```json
{
  "total_books": 42,
  "average_price": 22.50,
  "distribution_rating": [
    {
      "rating": "5",
      "count": 15
    },
    {
      "rating": "4",
      "count": 18
    },
    {
      "rating": "3",
      "count": 9
    }
  ]
}
```

#### Estatísticas por Categoria
```http
GET /stats/categories
```

**Response (200 OK):**
```json
[
  {
    "category": "Fiction",
    "total_books": 18,
    "average_price": 19.99
  },
  {
    "category": "Mystery",
    "total_books": 12,
    "average_price": 24.99
  },
  {
    "category": "Science Fiction",
    "total_books": 12,
    "average_price": 22.50
  }
]
```

### 🤖 Machine Learning - `/ml`

#### Obter Features Disponíveis
```http
GET /ml/features
```

**Response (200 OK):**
```json
[
  {
    "stock": 0,
    "rating": 0,
    "category_Fiction": 1,
    "category_Mystery": 0,
    "category_Science Fiction": 0
  }
]
```

#### Obter Dados de Treinamento
```http
GET /ml/training-data
```

**Response (200 OK):**
```json
[
  {
    "stock": 10,
    "rating": 4,
    "category_Fiction": 1,
    "category_Mystery": 0,
    "category_Science Fiction": 0,
    "price": 19.99
  }
]
```

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
- `401 Unauthorized`: Token JWT inválido
- `500 Internal Server Error`: Erro durante o treinamento

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
  "predicted_price": 21.50
}
```

**Errors:**
- `400 Bad Request`: Campos obrigatórios faltando
- `500 Internal Server Error`: Erro na predição

#### Avaliar Modelo
```http
GET /ml/evaluate
```

**Response (200 OK):**
```json
{
  "mse": 2.34,
  "rmse": 1.53,
  "r2_score": 0.87
}
```

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

## 📱 Exemplos de Uso com CURL

### Registrar um Novo Usuário
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "senha123"}'
```

### Fazer Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "senha123"}'
```

### Listar Todos os Livros
```bash
curl http://localhost:5000/books/
```

### Obter Detalhes de um Livro
```bash
curl http://localhost:5000/books/1
```

### Buscar Livros com Filtros
```bash
curl "http://localhost:5000/books/search?title=harry&min_price=10&max_price=30"
```

### Obter Categorias Disponíveis
```bash
curl http://localhost:5000/books/categories
```

### Obter Features de ML
```bash
curl http://localhost:5000/ml/features
```

### Obter Dados de Treinamento
```bash
curl http://localhost:5000/ml/training-data
```

### Treinar Modelo de ML (com token)
```bash
curl -X POST http://localhost:5000/ml/train-model \
  -H "Authorization: Bearer <seu-token-jwt>"
```

### Fazer Predição de Preço
```bash
curl -X POST http://localhost:5000/ml/predict \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Fiction",
    "stock": 10,
    "rating": 4
  }'
```

### Exemplos com Python Requests
```python
import requests

BASE_URL = "http://localhost:5000"

# Registrar usuário
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={"username": "john_doe", "password": "senha123"}
)
print(response.json())

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "john_doe", "password": "senha123"}
)
token = response.json()["access_token"]

# Listar livros
response = requests.get(f"{BASE_URL}/books/")
print(response.json())

# Treinar modelo (com token)
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/ml/train-model", headers=headers)
print(response.json())

# Buscar livros com filtros
response = requests.get(
    f"{BASE_URL}/books/search",
    params={"title": "Harry", "min_price": 10, "max_price": 30}
)
print(response.json())

# Obter categorias
response = requests.get(f"{BASE_URL}/books/categories")
print(response.json())

# Obter features de ML
response = requests.get(f"{BASE_URL}/ml/features")
print(response.json())

# Obter dados de treinamento
response = requests.get(f"{BASE_URL}/ml/training-data")
print(response.json())

# Fazer predição
response = requests.post(
    f"{BASE_URL}/ml/predict",
    json={"category": "Fiction", "stock": 10, "rating": 4}
)
print(response.json())

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

```

## 🔄 Fluxo de Uso para Cientistas de Dados/ML

### 1. Coleta de Dados
```
Web Scraper (Scrapy) → Extração de livros → Armazenamento em DB
```

### 2. Acesso aos Dados
```bash
# Obter features disponíveis
GET /ml/features

# Obter dados de treinamento
GET /ml/training-data
```

### 3. Treinamento do Modelo
```bash
# Treinar modelo RandomForest
POST /ml/train-model (requer autenticação)
```

### 4. Produção - Fazer Predições
```bash
# Usar modelo treinado para predições
POST /ml/predict
```

### 5. Análise de Resultados
```bash
# Obter estatísticas agregadas
GET /stats/overview
GET /stats/categories
```

## 🛠️ Estrutura do Projeto

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
└── instance/                # Arquivos de instância (não versionados)
    ├── user.db              # Banco de dados SQLite
    ├── ml_model.joblib      # Modelo ML treinado
    ├── encoder.joblib       # Encoder OneHot
    └── feature_order.joblib # Ordem das features
```

## 🔐 Segurança

- **Autenticação JWT**: Tokens com expiração de 30 minutos
- **Validação de Entrada**: Todos os inputs são validados
- **Tratamento de Erros**: Respostas padronizadas com códigos HTTP apropriados
- **Variáveis de Ambiente**: Chaves sensíveis não são versionadas
- **CORS**: Configurável para produção

## 🚀 Execução da Aplicação

### Modo Desenvolvimento
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

### Modo Produção
```bash
# Usar Gunicorn (instalar separadamente se necessário)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📊 Machine Learning - Detalhes Técnicos

### Modelo
- **Algoritmo**: RandomForest Regressor
- **Features**: Stock, Rating, Category (one-hot encoded)
- **Target**: Preço do livro

### Pipeline de Features
1. **Encoding**: One-Hot Encoding para categorias
2. **Normalização**: Escalamento de features numéricas
3. **Treinamento**: Divisão 80/20 (treino/teste)
4. **Validação**: Métricas MSE, RMSE, R²

### Melhorias Futuras para ML
- Implementação de múltiplos modelos (Gradient Boosting, XGBoost)
- Cross-validation para validação robusta
- Hyperparameter tuning automático
- API para A/B testing de modelos
- Versionamento de modelos
- Monitoramento de model drift

## 📈 Escalabilidade

### Arquitetura Pensada para Crescimento

1. **Camadas Separadas**: Fácil substituição de componentes
2. **Microserviços Prontos**: Serviços podem ser isolados
3. **Banco de Dados**: Suporta migração SQLite → PostgreSQL
4. **Cache**: Pronto para Redis
5. **Queue**: Suporta integração com Celery para tarefas assíncronas
6. **Monitoramento**: Estrutura para logging e APM

### Próximos Passos (Pretendo continuar o projeto após a entrega do Tech Challenge)
- [ ] Migrar para PostgreSQL
- [ ] Implementar Redis para cache
- [ ] Adicionar Celery para tarefas assíncronas
- [ ] Containerizar com Docker
- [ ] Deploy em Kubernetes
- [ ] Adicionar CI/CD com GitHub Actions

## 🔗 Links Importantes

- **Deploy**: [Link do Deploy] *(a ser preenchido)*
- **Vídeo Demonstração**: [Link do Vídeo] *(a ser preenchido)*
- **Documentação Swagger**: Disponível em `/api/docs` quando a aplicação estiver rodando

## 📝 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_URI` | Connection string do banco de dados | `sqlite:///user.db` |
| `SECRET_KEY` | Chave para sessões Flask | - |
| `JWT_SECRET_KEY` | Chave para assinar JWT | - |
| `FLASK_ENV` | Ambiente (development/production) | `development` |
| `FLASK_DEBUG` | Ativar modo debug | `True` |

## 📦 Dependências Principais

- **Flask**: Framework web
- **Flask-SQLAlchemy**: ORM para banco de dados
- **Flask-JWT-Extended**: Autenticação JWT
- **Flask-RESTx**: Documentação OpenAPI
- **Scrapy**: Web scraping
- **scikit-learn**: Machine Learning
- **joblib**: Serialização de modelos ML

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

