import pytest
from api.app import create_app 

@pytest.fixture
def app():
    """
    Cria uma instância da aplicação Flask para testes
    """
    app = create_app() 
    app.config.update({
        "TESTING": True,      
        "JWT_SECRET_KEY": "super-secret-key" 
    })

    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """
    Cria um client de testes para fazer requests à API
    """
    return app.test_client()
