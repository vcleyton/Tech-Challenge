from flask import Blueprint, jsonify, request
from src.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    user = data['username']
    password = data['password']

    service.register_user(user, password)

    return jsonify({"message": "User registered successfully"}), 201
