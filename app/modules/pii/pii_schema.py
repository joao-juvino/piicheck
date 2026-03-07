from marshmallow import Schema, fields


class PiiScanSchema(Schema):

    text = fields.String(required=True)