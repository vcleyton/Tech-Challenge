# 🔌 Design da API – Documento Auxiliar

> 📌 **Observação**: Este arquivo tem caráter **auxiliar** e serve como apoio ao entendimento técnico da API. Ele não substitui o README oficial do projeto.

---

## Visão Geral

Este documento descreve as **decisões de design**, **princípios arquiteturais** e a **estrutura dos endpoints** da API responsável por expor os dados do pipeline. O foco está na clareza, padronização e aderência a boas práticas de APIs modernas.

---

## 🎯 Objetivos do Design

* Garantir uma API simples, consistente e previsível
* Facilitar integração com aplicações externas
* Manter versionamento e evolução controlada
* Servir como base para expansão futura

---

## 🧩 Princípios Arquiteturais

A API foi projetada seguindo princípios amplamente adotados no mercado:

* **RESTful**: uso correto de recursos e verbos HTTP
* **Versionamento explícito**: `/api/v1`, permitindo evolução sem breaking changes
* **Formato JSON**: padrão de troca de dados
* **HTTP Status Codes**: comunicação clara de sucesso e erro
* **Stateless**: cada requisição é independente

---

## 🛣️ Estrutura de Endpoints

### Endpoints Principais

Responsáveis pelo acesso direto aos dados do domínio.

* `GET /api/v1/books`
  Retorna a lista de livros disponíveis

* `GET /api/v1/books/{id}`
  Retorna os detalhes de um livro específico

* `GET /api/v1/categories`
  Retorna as categorias cadastradas

* `GET /api/v1/health`
  Endpoint de verificação de saúde da aplicação

---

### Endpoints Opcionais / Evolutivos

Endpoints planejados para futuras expansões da API.

* 📊 Estatísticas agregadas
* 🔍 Filtros avançados (preço, categoria, rating)
* 🏆 Ranking de categorias ou livros

> 🔎 Esses endpoints não são obrigatórios para o funcionamento inicial, mas demonstram capacidade de evolução do projeto.

---

## 🔐 Segurança

A API prevê mecanismos básicos de segurança, podendo ser ativados conforme o contexto de uso.

* Autenticação baseada em **JWT (JSON Web Token)**
* Proteção de rotas sensíveis
* Separação entre endpoints públicos e privados

---

## 📚 Documentação da API

A documentação técnica da API é gerada automaticamente utilizando:

* **Swagger / OpenAPI** integrado à aplicação

**Benefícios:**

* Visualização interativa dos endpoints
* Testes diretos via interface web
* Facilidade de onboarding para novos desenvolvedores

---

