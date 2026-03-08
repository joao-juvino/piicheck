from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint

from app.extensions.extensions import limiter
from app.modules.auth.auth_schema import (
    AccessTokenSchema,
    LoginResponseSchema,
    LoginSchema,
    LogoutResponseSchema,
    MeResponseSchema,
    RegisterResponseSchema,
    RegisterSchema,
)
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
    @auth_blp.response(201, RegisterResponseSchema)
    def post(self, data):
        """
        Register a new user.

        Creates a user account using email and password.
        """

        user = AuthService.register(data["email"], data["password"])

        return {"id": user.id, "email": user.email}


@auth_blp.route("/login")
class LoginResource(MethodView):

    @limiter.limit("5 per minute")
    @auth_blp.arguments(LoginSchema)
    @auth_blp.response(200, LoginResponseSchema)
    def post(self, data):
        """
        Authenticate user.

        Returns:
        - access_token
        - refresh_token
        """

        access_token, refresh_token = AuthService.login(
            data["email"],
            data["password"]
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


@auth_blp.route("/refresh")
class RefreshResource(MethodView):

    @jwt_required(refresh=True)
    @auth_blp.response(200, AccessTokenSchema)
    def post(self):
        """
        Generate a new access token using a refresh token.
        """

        user_id = get_jwt_identity()

        access_token = AuthService.refresh(user_id)

        return {"access_token": access_token}


@auth_blp.route("/me")
class MeResource(MethodView):

    @jwt_required()
    @auth_blp.response(200, MeResponseSchema)
    def get(self):
        """
        Return information about the authenticated user.
        """

        user_id = get_jwt_identity()

        return {"user_id": user_id}


@auth_blp.route("/logout")
class LogoutResource(MethodView):

    @jwt_required()
    @auth_blp.response(200, LogoutResponseSchema)
    def post(self):
        """
        Logout user by revoking the current token.
        """

        return AuthService.logout()