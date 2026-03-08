from xml.dom import ValidationErr

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions.extensions import limiter
from app.modules.auth.auth_schema import LoginSchema, RegisterSchema
from app.modules.auth.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

register_schema = RegisterSchema()
login_schema = LoginSchema()

@auth_bp.route("/register", methods=["POST"])
def register():

    try:
        data = register_schema.load(request.json)

    except ValidationErr as err:
        return jsonify(err.messages), 400

    user = AuthService.register(
        data["email"],
        data["password"]
    )

    return jsonify({
        "id": user.id,
        "email": user.email
    })


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():

    try:
        data = login_schema.load(request.json)

    except ValidationErr as err:
        return jsonify(err.messages), 400

    token, refresh_token = AuthService.login(
        data["email"],
        data["password"]
    )

    return jsonify({
        "access_token": token,
        "refresh_token": refresh_token
    })


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    access_token = AuthService.refresh(user_id)

    return jsonify({
        "access_token": access_token
    })


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():

    user_id = get_jwt_identity()

    return jsonify({
        "user_id": user_id
    })

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    return AuthService.logout(), 200

