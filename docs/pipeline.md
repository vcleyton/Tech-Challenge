# 📊 Pipeline de Dados – Arquitetura Profissional


## 🎯 Objetivos do Projeto

* Demonstrar uma arquitetura de dados moderna e bem estruturada
* Garantir qualidade e padronização dos dados
* Facilitar consumo analítico e integração via API
* Servir como base para evolução em projetos de dados reais

---

## 🏗️ Arquitetura do Pipeline

O pipeline foi projetado de forma modular, com separação clara de responsabilidades entre as camadas, garantindo **manutenibilidade**, **escalabilidade** e **facilidade de evolução**.

---

### 🔹 1. Ingestão de Dados

Camada responsável pela coleta automatizada dos dados diretamente da fonte.

**Fonte:**
[https://books.toscrape.com](https://books.toscrape.com)

**Dados coletados:**

* 📘 Título do livro
* 💰 Preço
* ⭐ Avaliação (rating)
* 📦 Disponibilidade em estoque
* 🗂️ Categoria
* 🖼️ URL da imagem

**Boas práticas aplicadas:**

* Extração estruturada e padronizada
* Código resiliente a pequenas mudanças de layout
* Coleta de dados brutos para rastreabilidade

---

### 🔹 2. Processamento e Tratamento

Responsável por transformar dados brutos em dados confiáveis, consistentes e prontos para consumo.

**Principais transformações:**

* Normalização e conversão de preços
* Conversão de rating textual para valores numéricos
* Tratamento de encoding e caracteres especiais
* Padronização de tipos e nomenclatura de campos

**Benefícios:**

* Melhoria significativa da qualidade dos dados
* Redução de inconsistências e erros
* Preparação ideal para análises e modelos de Machine Learning

---

### 🔹 3. Persistência dos Dados

Camada de armazenamento responsável por manter os dados tratados de forma estruturada e acessível.

**Tecnologia:**

* SQLite

**Características:**

* Estrutura relacional organizada
* Dados prontos para consultas analíticas
* Fácil portabilidade e versionamento

> 🔎 A escolha do SQLite visa simplicidade e demonstração técnica, podendo ser facilmente substituído por PostgreSQL, MySQL ou outro banco relacional em ambientes produtivos.

---

### 🔹 4. Exposição via API

Os dados armazenados são disponibilizados através de uma **API RESTful**, promovendo desacoplamento entre dados e aplicações consumidoras.

**Tecnologias e padrões:**

* Flask
* Endpoints REST versionados (`/api/v1`)
* Respostas em formato JSON

**Vantagens:**

* Integração simples com front-ends e serviços externos
* Base sólida para escalabilidade
* Reutilização dos dados por múltiplos consumidores

---

### 🔹 5. Consumo dos Dados

Camada onde os dados geram valor direto para o negócio ou para análises técnicas.

**Casos de uso possíveis:**

* 📈 Dashboards analíticos
* 🤖 Pipelines de Machine Learning
* 🎯 Sistemas de recomendação
* 🔗 Integração com outros serviços e aplicações

---

## ⭐ Diferenciais do Projeto

* Pipeline completo (end-to-end)
* Arquitetura clara, modular e profissional
* Aplicação de boas práticas de engenharia de dados
* Fácil adaptação para novos cenários e fontes
* Ideal para projetos reais e portfólio técnico

---

## 🚀 Possíveis Evoluções Futuras

* Migração para PostgreSQL ou outro banco relacional
* Orquestração com Apache Airflow
* Containerização com Docker
* Implementação de testes automatizados
* Monitoramento e logging estruturado
* Autenticação e controle de acesso na API

---

