from app.extensions.extensions import db


class PiiDetection(db.Model):

    __tablename__ = "pii_detections"

    id = db.Column(db.Integer, primary_key=True)

    scan_id = db.Column(
        db.Integer,
        db.ForeignKey("pii_scans.id"),
        nullable=False
    )

    pii_type = db.Column(db.String(50), nullable=False)

    value = db.Column(db.String(255))

    start_position = db.Column(db.Integer)

    end_position = db.Column(db.Integer)