from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):

    email = fields.Email(
        required=True
    )

    password = fields.String(
        required=True,
        validate=validate.Length(min=6)
    )


class LoginSchema(Schema):

    email = fields.Email(required=True)

    password = fields.String(required=True)