from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):

    email = fields.Email(
        required=True,
        metadata={"example": "user@email.com"}
    )

    password = fields.String(
        required=True,
        validate=validate.Length(min=6),
        metadata={"example": "123456"}
    )


class LoginSchema(Schema):

    email = fields.Email(
        required=True,
        metadata={"example": "user@email.com"}
    )

    password = fields.String(
        required=True,
        metadata={"example": "123456"}
    )


class RegisterResponseSchema(Schema):

    id = fields.Int(metadata={"example": 3})
    email = fields.Email(metadata={"example": "user@email.com"})


class LoginResponseSchema(Schema):

    access_token = fields.String(
        metadata={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
    )

    refresh_token = fields.String(
        metadata={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
    )


class AccessTokenSchema(Schema):

    access_token = fields.String(
        metadata={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
    )


class MeResponseSchema(Schema):

    user_id = fields.String(
        metadata={"example": "3"}
    )


class LogoutResponseSchema(Schema):

    msg = fields.String(
        metadata={"example": "Successfully logged out"}
    )