from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from src.repository.user_repository import UserRepository
from src.config.config import Config
from src.utils.validators import Validator
from src.utils.exceptions import ConflictError, UnauthorizedError, ValidationError


class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, user, password):
        """
        Registra um novo usuário.
        
        Args:
            user (str): Nome de usuário
            password (str): Senha do usuário
            
        Returns:
            dict: Dados do usuário registrado (id e username)
            
        Raises:
            ValidationError: Se os dados forem inválidos
            ConflictError: Se o usuário já existe
        """
        # Valida entrada
        try:
            Validator.validate_username(user)
            Validator.validate_password(password)
        except ValidationError as e:
            raise ValidationError(str(e))
        
        # Verifica se usuário já existe
        if self.repo.get_user_by_username(user):
            raise ConflictError("Username já existe na base de dados")

        # Registra novo usuário
        hashed_password = generate_password_hash(password)
        new_user = self.repo.add_user(user, hashed_password)

        return {"id": new_user.id, "username": new_user.username}
    
    def login_user(self, username, password):
        """
        Autentica um usuário.
        
        Args:
            username (str): Nome de usuário
            password (str): Senha do usuário
            
        Returns:
            dict: Token de acesso JWT
            
        Raises:
            ValidationError: Se os dados forem inválidos
            UnauthorizedError: Se as credenciais forem inválidas
        """
        # Valida entrada
        try:
            Validator.validate_username(username)
            Validator.validate_password(password)
        except ValidationError as e:
            raise ValidationError(str(e))

        # Verifica credenciais
        user = self.repo.get_user_by_username(username)

        if not user or not check_password_hash(user.password, password):
            raise UnauthorizedError("Username ou password inválidos")

        # Gera token
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=Config.JWT_ACCESS_TOKEN_EXPIRES
        )

        return {"access_token": access_token}