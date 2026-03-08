# app/modules/auth/auth_routes.py
from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions.extensions import limiter
from app.modules.auth.auth_schema import RegisterSchema, LoginSchema
from app.modules.auth.auth_service import AuthService

auth_blp = Blueprint(
    "auth",
    "auth",
    url_prefix="/auth",
    description="Authentication endpoints"
)

@auth_blp.route("/register")
class RegisterResource(MethodView):

    @auth_blp.arguments(RegisterSchema)
    @auth_blp.response(201)
    def post(self, data):
        """
        Register a new user.
        Request validated by RegisterSchema.
        """
        user = AuthService.register(data["email"], data["password"])

        return {"id": user.id, "email": user.email}


@auth_blp.route("/login")
class LoginResource(MethodView):

    @limiter.limit("5 per minute")
    @auth_blp.arguments(LoginSchema)
    @auth_blp.response(200)
    def post(self, data):
        """
        Login -> returns access_token and refresh_token.
        """
        access_token, refresh_token = AuthService.login(data["email"], data["password"])
        return {"access_token": access_token, "refresh_token": refresh_token}


@auth_blp.route("/refresh")
class RefreshResource(MethodView):

    @jwt_required(refresh=True)
    @auth_blp.response(200)
    def post(self):
        """
        Use refresh token to get a new access token.
        """
        user_id = get_jwt_identity()
        access_token = AuthService.refresh(user_id)
        return {"access_token": access_token}


@auth_blp.route("/me")
class MeResource(MethodView):

    @jwt_required()
    @auth_blp.response(200)
    def get(self):
        """
        Return authenticated user id (example).
        """
        user_id = get_jwt_identity()
        return {"user_id": user_id}


@auth_blp.route("/logout")
class LogoutResource(MethodView):

    @jwt_required()
    @auth_blp.response(200)
    def post(self):
        """
        Revoke current access token (logout).
        """
        return AuthService.logout()