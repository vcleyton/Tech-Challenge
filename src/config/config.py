import os
from dotenv import load_dotenv
from datetime import timedelta
from pathlib import Path

# Carrega variáveis do arquivo .env na raiz do projeto
load_dotenv()

# Define o diretório base (raiz do projeto)
BASE_DIR = Path(__file__).parent.parent.resolve()

class Config:
    # Configuração do banco de dados SQLite
    DB_PATH = BASE_DIR / os.getenv('DATABASE_FILE_PATH', 'databases/user.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de segurança
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret')
    JWT_TOKEN_LOCATION = os.getenv('JWT_TOKEN_LOCATION', 'headers')
    
    # Configuração do tempo de expiração do token JWT
    try:
        _expires_seconds = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_SECONDS', 1800))
    except ValueError:
        _expires_seconds = 1800
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=_expires_seconds)