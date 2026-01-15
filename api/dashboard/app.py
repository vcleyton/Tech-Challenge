import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")

st.title("📊 Books Tech Challenge - Dashboard")

try:
    response = requests.get(f"{API_BASE_URL}/api/v1/books/stats", timeout=10)
    response.raise_for_status()
    data = response.json()

    st.metric("Total de Livros", data["total_books"])
    st.metric("Preço Médio", data["avg_price"])
    st.metric("Rating Médio", data["avg_rating"])

except Exception as e:
    st.error("Erro ao conectar com a API")
    st.exception(e)



