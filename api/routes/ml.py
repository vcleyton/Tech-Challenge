from flask_restx import Namespace, Resource, fields
from flask import request
from api.database import get_db_connection

api = Namespace("ml", description="Endpoints para consumo de dados de ML")

# Modelo opcional para predições recebidas (Swagger)
prediction_model = api.model("Prediction", {
    "id": fields.Integer(required=True, description="ID do livro"),
    "predicted_rating": fields.Float(required=True, description="Predição de rating")
})


@api.route("/features")
class MLFeatures(Resource):
    @api.doc(description="Retorna os dados de features para treinamento ML")
    def get(self):
        conn = get_db_connection()
        books = conn.execute("""
            SELECT
                price,
                rating,
                CASE WHEN availability > 0 THEN 1 ELSE 0 END AS available
            FROM books
        """).fetchall()
        conn.close()

        return [dict(row) for row in books]

@api.route("/training-data")
class MLTrainingData(Resource):
    @api.doc(description="Retorna todos os dados para treinamento de ML")
    def get(self):
        conn = get_db_connection()
        books = conn.execute("SELECT * FROM books").fetchall()
        conn.close()

        return [dict(row) for row in books]


@api.route("/predictions")
class MLPredictions(Resource):
    @api.doc(description="Recebe predições de ML")
    @api.expect([prediction_model], validate=True)
    def post(self):
        data = request.get_json()

        # Aqui você poderia salvar no banco ou processar
        return {
            "msg": "Predições recebidas com sucesso",
            "received": data
        }
