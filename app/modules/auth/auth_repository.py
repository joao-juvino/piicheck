from app.extensions.extensions import db
from app.modules.auth.auth_model import User
from app.modules.auth.token_blocklist_model import TokenBlocklist


class AuthRepository:

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(email, password_hash):

        user = User(
            email=email,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        return user
    
    @staticmethod
    def add_token_to_blocklist(jti):

        token = TokenBlocklist(jti=jti)

        db.session.add(token)
        db.session.commit()

        return token

    @staticmethod
    def is_token_revoked(jti):

        token = TokenBlocklist.query.filter_by(jti=jti).first()

        return token is not None