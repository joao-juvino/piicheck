from flask_jwt_extended import create_access_token, create_refresh_token
from app.modules.auth.auth_repository import AuthRepository
from app.utils.password import hash_password, verify_password
from flask_jwt_extended import get_jwt


class AuthService:

    @staticmethod
    def register(email, password):

        existing_user = AuthRepository.get_user_by_email(email)

        if existing_user:
            raise Exception("User already exists")

        password_hash = hash_password(password)

        user = AuthRepository.create_user(email, password_hash)

        return user

    @staticmethod
    def login(email, password):

        user = AuthRepository.get_user_by_email(email)

        if not user:
            raise Exception("Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise Exception("Invalid credentials")

        token = create_access_token(identity=str(user.id))

        refresh_token = create_refresh_token(identity=str(user.id))

        return token, refresh_token
    
    @staticmethod
    def refresh(user_id):
        token = create_access_token(identity=str(user_id))
        return token
    
    @staticmethod
    def logout():

        jwt_payload = get_jwt()

        jti = jwt_payload["jti"]

        AuthRepository.add_token_to_blocklist(jti)

        return {"msg": "Successfully logged out"}

