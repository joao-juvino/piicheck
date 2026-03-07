from flask_jwt_extended import get_jwt
from app.extensions.extensions import jwt
from app.modules.auth.token_blocklist_model import TokenBlocklist


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):

    jti = jwt_payload.get("jti")

    if jti is None:
        return True

    token = TokenBlocklist.query.filter_by(jti=jti).first()

    return token is not None


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return {"msg": "Token has been revoked"}, 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {"msg": "Token has expired"}, 401


@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return {"msg": f"Invalid token: {reason}"}, 422


@jwt.unauthorized_loader
def missing_token_callback(reason):
    return {"msg": f"Missing token: {reason}"}, 401
