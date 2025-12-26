from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

# Usuário fake (suficiente para o challenge)
USERS = {
    "admin": "admin123"
}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if USERS.get(username) != password:
        return jsonify({"msg": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token
    )

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)

    return jsonify(access_token=new_access_token)
