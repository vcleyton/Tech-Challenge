from .health import health_bp
from .books import books_bp
from .stats import stats_bp
from .auth import auth_bp

def register_blueprints(app):
    """Registra todas as Blueprints da aplicação."""

    app.register_blueprint(health_bp, url_prefix='/health')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(stats_bp, url_prefix='/stats')
    app.register_blueprint(auth_bp, url_prefix='/auth')