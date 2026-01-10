import os
from dotenv import load_dotenv
from datetime import timedelta

# Carrega variáveis do arquivo .env na raiz do projeto
load_dotenv()

class Config:
    # Configuração do banco de dados SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///user.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de segurança
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Configuração do tempo de expiração do token JWT
    try:
        _expires_seconds = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_SECONDS', 1800))
    except ValueError:
        _expires_seconds = 1800
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=_expires_seconds)