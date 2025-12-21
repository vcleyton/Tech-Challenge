from flask_restx import Namespace, Resource
from api.database import get_db_connection

api = Namespace("health", description="Health check da API")


@api.route("/")
class Health(Resource):
    def get(self):
        """
        Verifica se a API e o banco estão funcionando.
        """
        try:
            conn = get_db_connection()
            conn.execute("SELECT 1")
            conn.close()
            return {"status": "ok"}, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500
