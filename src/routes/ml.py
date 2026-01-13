"""
Rotas de Machine Learning - Treina modelo e faz predições de preço.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.services.ml_service import MLService
from src.utils.exceptions import ValidationError, MLError

ml_bp = Blueprint('ml', __name__)

service = MLService()

@ml_bp.route('/features', methods=['GET'])
def get_features():
    """
    Retorna as features (características) disponíveis para o modelo.
    
    ---
    tags:
      - Machine Learning
    responses:
      200:
        description: Lista de features codificadas
        schema:
          type: array
          items:
            type: object
            properties:
              stock:
                type: integer
              rating:
                type: integer
              category_*:
                type: number
                description: Feature one-hot encoded para categoria
    """
    try:
        features = service.get_features()
        return jsonify(features), 200
    except MLError as e:
        return jsonify({"message": str(e), "error": "MLError"}), 500
    except Exception as e:
        return jsonify({"message": "Erro ao buscar features", "error": "InternalServerError"}), 500


@ml_bp.route('/training-data', methods=['GET'])
def get_training_data():
    """
    Retorna os dados de treinamento do modelo.
    
    ---
    tags:
      - Machine Learning
    responses:
      200:
        description: Dados de treinamento com features e preço alvo
        schema:
          type: array
          items:
            type: object
            properties:
              stock:
                type: integer
              rating:
                type: integer
              price:
                type: number
              category_*:
                type: number
                description: Feature one-hot encoded para categoria
    """
    try:
        training_data = service.get_training_data()
        return jsonify(training_data), 200
    except MLError as e:
        return jsonify({"message": str(e), "error": "MLError"}), 500
    except Exception as e:
        return jsonify({"message": "Erro ao buscar dados de treinamento", "error": "InternalServerError"}), 500


@ml_bp.route('/train-model', methods=['POST'])
@jwt_required()
def train_model():
    """
    Treina o modelo de Machine Learning (RandomForest Regressor).
    
    Requer autenticação JWT.
    
    ---
    tags:
      - Machine Learning
    security:
      - Bearer: []
    responses:
      200:
        description: Modelo treinado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Model trained successfully"
      401:
        description: Não autorizado - Token JWT inválido
      500:
        description: Erro ao treinar o modelo
    """
    try:
        service.train_model()
        return jsonify({"message": "Modelo treinado com sucesso"}), 200
    except MLError as e:
        return jsonify({"message": str(e), "error": "MLError"}), 500
    except Exception as e:
        return jsonify({"message": "Erro ao treinar o modelo", "error": "InternalServerError"}), 500


@ml_bp.route('/predict', methods=['POST'])
def predict():
    """
    Realiza predição de preço para um livro baseado em suas características.
    
    ---
    tags:
      - Machine Learning
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            category:
              type: string
              description: Categoria do livro
              example: "Fiction"
            stock:
              type: integer
              description: Quantidade em estoque
              example: 10
            rating:
              type: integer
              description: Avaliação do livro (0-5)
              example: 4
          required:
            - category
            - stock
            - rating
    responses:
      200:
        description: Predição realizada com sucesso
        schema:
          type: object
          properties:
            predicted_price:
              type: number
              description: Preço predito para o livro
              example: 29.99
      400:
        description: Dados de entrada inválidos
        schema:
          type: object
          properties:
            message:
              type: string
            error:
              type: string
      500:
        description: Erro durante a predição
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
        
        prediction = service.predict(data)
        return jsonify(prediction), 200
    
    except ValidationError as e:
        return jsonify({"message": str(e), "error": "ValidationError"}), 400
    except MLError as e:
        return jsonify({"message": str(e), "error": "MLError"}), 500
    except Exception as e:
        return jsonify({"message": "Erro ao realizar predição", "error": "InternalServerError"}), 500
