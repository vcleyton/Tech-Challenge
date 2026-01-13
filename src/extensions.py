"""
Extensões da aplicação Flask.
Define instâncias de extensões que são inicializadas no app.

Este arquivo segue o padrão de aplicação de dois estágios (two-stage initialization pattern):
1. Criar instância da extensão (aqui)
2. Inicializar a extensão no app (em __init__.py)

Isso permite evitar circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Instância do SQLAlchemy para ORM
# Será inicializada em __init__.py
db = SQLAlchemy()

# Instância do JWTManager para autenticação JWT
# Será inicializada em __init__.py
jwt = JWTManager()