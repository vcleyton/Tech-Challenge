from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from src.repository.user_repository import UserRepository
from src.config.config import Config
from src.extensions import db
from src.models.user import User

class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, user, password):
        
        if self.repo.get_user_by_username(user):
            raise ValueError("Username already exists")

        hashed_password = generate_password_hash(password)
        new_user = self.repo.add_user(user, hashed_password)

        return {"id": new_user.id, "username": new_user.username}
    
    def login_user(self, username, password):
        user = self.repo.get_user_by_username(username)

        if not user or not check_password_hash(user.password, password):
            raise ValueError("Invalid username or password")

        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=Config.JWT_ACCESS_TOKEN_EXPIRES
        )

        return {"access_token": access_token}