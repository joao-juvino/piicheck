from marshmallow import Schema, fields


class FileUploadSchema(Schema):
    file = fields.Raw(
        required=True,
        metadata={
            "type": "string",
            "format": "binary",
            "description": "Plain text file (.txt) containing text to scan"
        }
    )


class ScanResponseSchema(Schema):
    scan_id = fields.Int(metadata={"example": 13})
    status = fields.Str(metadata={"example": "queued"})


class ScanItemSchema(Schema):
    scan_id = fields.Int(metadata={"example": 13})
    text = fields.Str(metadata={"example": "Meu CPF é 123.456.789-10"})
    created_at = fields.DateTime()


class ScansListSchema(Schema):
    items = fields.List(fields.Nested(ScanItemSchema))
    page = fields.Int(metadata={"example": 1})
    pages = fields.Int(metadata={"example": 1})
    total = fields.Int(metadata={"example": 8})


class DetectionSchema(Schema):
    id = fields.Int(metadata={"example": 19})
    type = fields.Str(metadata={"example": "cpf"})
    value = fields.Str(metadata={"example": "123.456.789-10"})
    start = fields.Int(metadata={"example": 10})
    end = fields.Int(metadata={"example": 24})


class ScanResultsSchema(Schema):
    scan_id = fields.Int(metadata={"example": 13})
    created_at = fields.DateTime()
    detections = fields.List(fields.Nested(DetectionSchema))