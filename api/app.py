from flask import Flask
from flask_restx import Api

from api.routes.books import api as books_ns
from api.routes.categories import api as categories_ns
from api.routes.health import api as health_ns

from api.routes.stats import stats_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(stats_bp)
    
    api = Api(
        app,
        title="Books Tech Challenge API",
        version="1.0",
        description="API pública para consulta de livros (Tech Challenge)"
    )

    # Registrando namespaces (rotas)
    api.add_namespace(books_ns, path="/api/v1/books")
    api.add_namespace(categories_ns, path="/api/v1/categories")
    api.add_namespace(health_ns, path="/api/v1/health")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
