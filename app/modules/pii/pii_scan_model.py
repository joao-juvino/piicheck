from datetime import datetime
from app.extensions.extensions import db


class PiiScan(db.Model):

    __tablename__ = "pii_scans"

    __table_args__ = (
        db.Index("idx_scan_user_created", "user_id", "created_at"),
    )

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    input_text = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        index=True
    )

    status = db.Column(
        db.String(20),
        default="pending"
    )

    detections = db.relationship(
        "PiiDetection",
        backref="scan",
        cascade="all, delete-orphan",
        lazy=True
    )