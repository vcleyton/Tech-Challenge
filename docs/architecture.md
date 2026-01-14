# 🏗️ Plano Arquitetural — Books Tech Challenge

Este documento descreve a arquitetura do **Books Tech Challenge**, detalhando o pipeline de dados, os componentes do sistema, as decisões arquiteturais e os cenários de evolução para **Machine Learning** e **escala em produção**.

---

## 1. 🎯 Visão Geral

O **Books Tech Challenge** é uma API de consulta de livros construída em **Python (Flask)**, projetada para suportar todo o ciclo de vida dos dados:

* **Ingestão** (scraping ou fontes externas)
* **Processamento e validação**
* **Persistência em banco de dados**
* **Exposição via API REST**
* **Consumo por aplicações, dashboards e pipelines de ML**

A arquitetura prioriza **modularidade**, **clareza** e **facilidade de evolução**, permitindo que cada componente seja substituído ou escalado de forma independente.

---

## 2. 🔄 Pipeline de Dados

O pipeline abaixo representa o fluxo completo da solução, desde a origem dos dados até o consumo final:

```
+------------------+    +---------------------+    +---------------------+    +------------------+
|  Scraping /      | -> | Processamento &     | -> | Banco de Dados      | -> | API REST         |
|  Ingestão        |    | Limpeza de Dados    |    | (SQLite / SQL)     |    | (Flask)          |
+------------------+    +---------------------+    +---------------------+    +------------------+
                                                                              |
                                                                              v
                                                                     +------------------+
                                                                     | Consumidores     |
                                                                     | - Dashboards     |
                                                                     | - Cientistas ML  |
                                                                     | - Serviços       |
                                                                     +------------------+
```

### Descrição do Fluxo

1. **Ingestão / Scraping**

   * Coleta dados de livros (título, preço, categoria, rating, disponibilidade).
   * Atualmente simulado para controle de escopo, mas preparado para scraping real ou integração externa.

2. **Processamento e Limpeza**

   * Normalização de campos.
   * Conversão de tipos (ex.: preço, rating).
   * Tratamento de valores inconsistentes.

3. **Banco de Dados**

   * Persistência estruturada dos dados.
   * Uso inicial de **SQLite**, com fácil migração para bancos relacionais mais robustos.

4. **API REST**

   * Exposição dos dados via endpoints organizados por domínio.
   * Documentação automática via Swagger.

5. **Consumo**

   * Acesso por dashboards analíticos.
   * Integração com pipelines de Machine Learning.
   * Consumo por serviços externos.

---

## 3. 🧩 Componentes do Sistema

* **Ingestão / Scraping**

  * Responsável pela coleta de dados.
  * Executado via endpoint protegido por JWT.

* **Camada de Processamento**

  * Responsável por validação e transformação dos dados.
  * Isolada da camada de API.

* **Banco de Dados**

  * Armazena os dados tratados.
  * Projetado para ser facilmente substituível.

* **API REST (Flask)**

  * Organizada em namespaces:

    * Books
    * Categories
    * Stats
    * Machine Learning
    * Auth
    * Scraping

* **Camada de Consumo**

  * Dashboards (Streamlit, Grafana).
  * Cientistas de dados e pipelines automatizados.

---

## 4. 📈 Arquitetura para Escalabilidade

Embora a implementação atual seja simples, a arquitetura foi desenhada para crescimento:

* **Banco de dados escalável**

  * Migração direta para PostgreSQL ou MySQL.

* **Serviços desacoplados**

  * Scraping, API e ML podem se tornar microserviços independentes.

* **Processamento assíncrono**

  * Uso de filas (Celery + RabbitMQ ou Kafka) para ingestão e tarefas pesadas.

* **Cache**

  * Redis ou Memcached para acelerar consultas frequentes.

* **Segurança**

  * Autenticação JWT para proteção de rotas sensíveis.
  * Possível integração com OAuth2 ou Identity Providers.

---

## 5. 🤖 Cenário de Uso para Cientistas de Dados / ML

A API fornece **contratos de dados claros** para uso em Machine Learning:

### Acesso a Features

* `GET /api/v1/ml/features`
* Retorna apenas colunas numéricas e indicadores prontos para modelagem.

### Dataset Completo

* `GET /api/v1/ml/training-data`
* Retorna todos os dados necessários para treinamento e análise exploratória.

### Envio de Predições

* `POST /api/v1/ml/predictions`
* Recebe resultados de modelos treinados para análises ou ciclos de feedback.

### Fluxo típico de ML

```
API -> Features -> Treinamento do Modelo -> Predições -> Métricas / Feedback
```

---

## 6. 🔌 Plano de Integração com Modelos de Machine Learning

### Exemplo de Features

```json
[
  {
    "price": 12.99,
    "rating": 5,
    "available": 1
  }
]
```

### Dataset Completo

```json
[
  {
    "id": 1,
    "title": "Clean Code",
    "price": 12.99,
    "rating": 5,
    "availability": "In stock",
    "category": "Programming",
    "image_url": "url",
    "product_url": "url"
  }
]
```

### Envio de Predições

```json
[
  {
    "id": 1,
    "predicted_rating": 4.8
  }
]
```

### Evoluções Futuras

* Treinamento de modelos diretamente a partir da API.
* Orquestração de pipelines com Airflow ou Prefect.
* Dashboards analíticos com Streamlit ou Grafana.
* Monitoramento de performance de modelos (MLOps).

---

## 7. 📌 Considerações Finais

* Arquitetura **modular e extensível**.
* Pipeline completo: ingestão → processamento → persistência → API → consumo.
* Preparada para **Machine Learning** e evolução para produção.
* Segurança, observabilidade e escalabilidade consideradas desde o design.

Este plano arquitetural garante que o projeto não seja apenas funcional, mas também **sustentável, profissional e pronto para crescimento**.
