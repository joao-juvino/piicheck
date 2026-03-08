from datetime import datetime

from app.extensions.extensions import db


class TokenBlocklist(db.Model):

    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)

    jti = db.Column(db.String(120), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )