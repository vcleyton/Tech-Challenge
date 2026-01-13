import joblib
import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from src.repository.books_repository import BooksRepository
from src.utils.validators import Validator
from src.utils.exceptions import ValidationError, MLError


class MLService:
    def __init__(self):
        self.repository = BooksRepository()
        
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.instance_path = os.path.join(self.base_path, 'instance')
        
        os.makedirs(self.instance_path, exist_ok=True)

    def get_features(self):
        """
        Retorna as features (características) disponíveis para o modelo.
        
        Returns:
            list: Lista de dicionários com features codificadas
            
        Raises:
            MLError: Se houver erro ao processar os dados
        """
        try:
            df_encoded = self.get_formatted_data(target=False)
            return df_encoded.to_dict(orient='records')
        except Exception as e:
            raise MLError(f"Erro ao obter features: {str(e)}")

    def get_training_data(self):
        """
        Retorna os dados de treinamento do modelo.
        
        Returns:
            list: Lista de dicionários com dados de treinamento
            
        Raises:
            MLError: Se houver erro ao processar os dados
        """
        try:
            df_encoded = self.get_formatted_data()
            return df_encoded.to_dict(orient='records')
        except Exception as e:
            raise MLError(f"Erro ao obter dados de treinamento: {str(e)}")

    def train_model(self):
        """
        Treina o modelo de Machine Learning.
        
        Raises:
            MLError: Se houver erro durante o treinamento
        """
        try:
            df_encoded = self.get_formatted_data()

            if len(df_encoded) == 0:
                raise MLError("Não há dados suficientes para treinar o modelo")

            X = df_encoded.drop('price', axis=1)
            y = df_encoded['price'] 

            from sklearn.ensemble import RandomForestRegressor

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)

            file_path = os.path.join(self.instance_path, 'ml_model.joblib')
            joblib.dump(model, file_path)
        except Exception as e:
            raise MLError(f"Erro ao treinar modelo: {str(e)}")

    def predict(self, predictions_json):
        """
        Realiza predição de preço para um livro.
        
        Args:
            predictions_json (dict): Dicionário com categoria, stock e rating
            
        Returns:
            dict: Dicionário com preço predito
            
        Raises:
            ValidationError: Se os dados de entrada forem inválidos
            MLError: Se houver erro na predição
        """
        try:
            # Valida entrada
            Validator.validate_prediction_input(predictions_json)
            
            df_input = pd.DataFrame([predictions_json])

            df_input["stock"] = df_input["stock"].astype(int)
            df_input["rating"] = df_input["rating"].astype(int)
            df_input["category"] = df_input["category"].astype(str).str.lower().str.strip()

            encoder_file_path = os.path.join(self.instance_path, 'encoder.joblib')
            model_file_path = os.path.join(self.instance_path, 'ml_model.joblib')

            if os.path.exists(encoder_file_path):
                df_encoded = self.encode_input(df_input)
            else:
                self.encode_predict_data()
                df_encoded = self.encode_input(df_input)

            if os.path.exists(model_file_path):
                model = joblib.load(model_file_path)
                prediction = model.predict(df_encoded)
                return {"predicted_price": round(float(prediction[0]), 2)}
            else:
                raise MLError("Modelo treinado não encontrado. Por favor, treine o modelo primeiro.")
        except ValidationError as e:
            raise e
        except Exception as e:
            raise MLError(f"Erro durante predição: {str(e)}")

    def get_formatted_data(self, target=True):
        """
        Formata dados dos livros para o modelo.
        
        Args:
            target (bool): Se True, inclui o preço (target)
            
        Returns:
            pd.DataFrame: DataFrame com dados formatados e codificados
            
        Raises:
            MLError: Se houver erro ao processar os dados
        """
        try:
            books = self.repository.get_books()

            if not books:
                raise MLError("Nenhum livro disponível na base de dados")

            if target:
                data = [ {
                    "category": book["category"].lower().strip(),
                    "stock": int(book["stock"]),
                    "rating": int(book["rating"]),
                    "price": float(book["price"])
                    } for book in books ]
            else:
                data = [ {
                    "category": book["category"].lower().strip(),
                    "stock": int(book["stock"]),
                    "rating": int(book["rating"])
                    } for book in books ]
                
            df = pd.DataFrame(data)
            df_encoded = self.encode_input(df)

            return df_encoded
        except Exception as e:
            raise MLError(f"Erro ao formatar dados: {str(e)}")
    
    def encode_predict_data(self):
        """
        Codifica dados de predição para o encoder.
        
        Raises:
            MLError: Se houver erro ao codificar
        """
        try:
            books = self.repository.get_books()

            if not books:
                raise MLError("Nenhum livro disponível para codificação")

            books_categories = [book["category"].lower().strip() for book in books]
        
            df_books = pd.DataFrame(books_categories, columns=['category'])

            self.encode_input(df_books)
        except Exception as e:
            raise MLError(f"Erro ao codificar dados de predição: {str(e)}")
        
    def encode_input(self, df_input):
        """
        Codifica features categóricas usando OneHotEncoder.
        
        Args:
            df_input (pd.DataFrame): DataFrame com dados para codificar
            
        Returns:
            pd.DataFrame: DataFrame com features codificadas
            
        Raises:
            MLError: Se houver erro na codificação
        """
        try:
            file_path = os.path.join(self.instance_path, 'encoder.joblib')

            if os.path.exists(file_path):
                encoder = joblib.load(file_path)
            else:
                encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
                encoder.fit(df_input[['category']])
                joblib.dump(encoder, file_path)
            
            df_encoded = pd.DataFrame(encoder.transform(df_input[['category']]), columns=encoder.get_feature_names_out(['category']))
            df_final = pd.concat([df_input.drop('category', axis=1), df_encoded], axis=1)

            return df_final
        except Exception as e:
            raise MLError(f"Erro ao codificar features: {str(e)}")
