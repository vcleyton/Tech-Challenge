from src.extensions import db

class User(db.Model):
    """Modelo de dados para a tabela 'user'."""
    
    # Nome da tabela no banco de dados
    __tablename__ = 'users' 

    # Colunas da tabela
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=True, nullable=False)