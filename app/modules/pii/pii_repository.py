from app.extensions.extensions import db
from app.modules.pii.pii_scan_model import PiiScan
from app.modules.pii.pii_detection_model import PiiDetection


class PiiRepository:

    @staticmethod
    def create_scan(user_id, text):

        scan = PiiScan(
            user_id=user_id,
            input_text=text,
            status="queued"
        )

        db.session.add(scan)
        db.session.flush()
        db.session.commit()

        return scan


    @staticmethod
    def add_detection(scan_id, item):

        detection = PiiDetection(
            scan_id=scan_id,
            pii_type=item["type"],
            value=item["value"],
            start_position=item["start"],
            end_position=item["end"]
        )

        db.session.add(detection)

    @staticmethod
    def get_user_scans(user_id, page=1, per_page=10):

        scans = (
            PiiScan.query
            .filter_by(user_id=user_id)
            .order_by(PiiScan.created_at.desc())
            .paginate(page=page, per_page=per_page)
        )

        return scans

    @staticmethod
    def get_scan_by_id(scan_id):

        return PiiScan.query.filter_by(id=scan_id).first()


    @staticmethod
    def get_scan_detections(scan_id):

        detections = (
            PiiDetection.query
            .filter_by(scan_id=scan_id)
            .all()
        )

        return detections
