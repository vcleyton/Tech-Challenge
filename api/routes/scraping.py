from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from flask import jsonify

api = Namespace("scraping", description="Operações de scraping de livros (admin)")

@api.route("/trigger")
class TriggerScraping(Resource):
    @jwt_required()
    @api.doc(
        description="Inicia o scraping de livros (rota protegida, somente admin)",
        security="Bearer Auth"
    )
    def post(self):
        return jsonify({
            "message": "Scraping iniciado com sucesso (mock)"
        })
