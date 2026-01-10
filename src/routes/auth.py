from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    user = data['username']
    password = data['password']

    if not user or not password:
        return jsonify({"message": "Username and password are required"}), 400

    try:
        service.register_user(user, password)
    except ValueError as e:
        if str(e) == "Username already exists":
            return jsonify({"message": str(e)}), 409
        
        return jsonify({"message": "Registration failed"}), 500
    
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    try:
        token_data = service.login_user(username, password)
    except ValueError as e:
        if str(e) == "Invalid username or password":
            return jsonify({"message": str(e)}), 401
        
        return jsonify({"message": "Login failed"}), 500

    return jsonify(token_data), 200