"""
Rotas de autenticação - Registra e autentica usuários.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.auth_service import AuthService
from src.utils.exceptions import ValidationError, ConflictError, UnauthorizedError

auth_bp = Blueprint('auth', __name__)

service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register_user():
    """
    Registra um novo usuário.
    
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Nome de usuário (3-50 caracteres, apenas letras, números, _ e -)
              example: "john_doe"
            password:
              type: string
              description: Senha (mínimo 6 caracteres)
              example: "senha123"
          required:
            - username
            - password
    responses:
      201:
        description: Usuário registrado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            username:
              type: string
      400:
        description: Validação de dados falhou
        schema:
          type: object
          properties:
            message:
              type: string
            error:
              type: string
      409:
        description: Username já existe
        schema:
          type: object
          properties:
            message:
              type: string
            error:
              type: string
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "JSON body obrigatório", "error": "BadRequest"}), 400

        username = data.get('username')
        password = data.get('password')

        service.register_user(username, password)
        return jsonify({"message": "Usuário registrado com sucesso"}), 201
    
    except ValidationError as e:
        return jsonify({"message": str(e), "error": "ValidationError"}), 400
    except ConflictError as e:
        return jsonify({"message": str(e), "error": "ConflictError"}), 409
    except Exception as e:
        return jsonify({"message": "Erro ao registrar usuário", "error": "InternalServerError"}), 500


@auth_bp.route('/login', methods=['POST'])
def login_user():
    """
    Autentica um usuário e retorna JWT token.
    
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Nome de usuário
              example: "john_doe"
            password:
              type: string
              description: Senha do usuário
              example: "senha123"
          required:
            - username
            - password
    responses:
      200:
        description: Login realizado com sucesso
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: Token JWT para autenticação
      400:
        description: Validação de dados falhou
        schema:
          type: object
          properties:
            message:
              type: string
            error:
              type: string
      401:
        description: Credenciais inválidas
        schema:
          type: object
          properties:
            message:
              type: string
            error:
              type: string
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "JSON body obrigatório", "error": "BadRequest"}), 400

        username = data.get('username')
        password = data.get('password')

        token_data = service.login_user(username, password)
        return jsonify(token_data), 200
    
    except ValidationError as e:
        return jsonify({"message": str(e), "error": "ValidationError"}), 400
    except UnauthorizedError as e:
        return jsonify({"message": str(e), "error": "UnauthorizedError"}), 401
    except Exception as e:
        return jsonify({"message": "Erro ao fazer login", "error": "InternalServerError"}), 500
