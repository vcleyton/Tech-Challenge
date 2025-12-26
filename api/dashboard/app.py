import streamlit as st
import requests

API_URL = "http://localhost:5000/api/v1/books/stats"

st.title("📊 Book API Analytics")

response = requests.get(API_URL).json()

st.metric("Total de Livros", response["total_books"])
st.metric("Preço Médio", response["avg_price"])
st.metric("Rating Médio", response["avg_rating"])
