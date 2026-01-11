from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from flask import jsonify

# Namespace RESTX
api = Namespace("scraping", description="Operações de scraping de livros (admin)")

# ==========================
# POST /api/v1/scraping/trigger
# ==========================
@api.route("/trigger")
class TriggerScraping(Resource):
    @jwt_required()
    @api.doc(
        description="Inicia o scraping de livros (rota protegida, somente admin)",
        security="Bearer Auth"
    )
    def post(self):
        # Aqui você pode chamar a função real de scraping
        # Por enquanto é um mock
        return jsonify({
            "message": "Scraping iniciado com sucesso (mock)"
        })
