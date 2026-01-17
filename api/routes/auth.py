from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

api = Namespace("auth", description="Autenticação e JWT")

login_model = api.model(
    "Login",
    {
        "username": fields.String(required=True, description="Nome do usuário"),
        "password": fields.String(required=True, description="Senha do usuário")
    }
)

USERS = {
    "admin": "admin123"
}

@api.route("/login")
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.doc(description="Obter token de acesso e refresh")
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if USERS.get(username) != password:
            return {"msg": "Credenciais inválidas"}, 401

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


@api.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    @api.doc(
        description="Renovar token de acesso usando refresh token",
        security="Bearer Auth"
    )
    def post(self):
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        return {"access_token": new_access_token}
