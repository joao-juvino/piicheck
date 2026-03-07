from app.modules.pii.pii_scan_model import PiiScan
from app.modules.pii.pii_tasks import process_scan
from flask_jwt_extended import get_jwt_identity

from app.modules.pii.pii_detector import PIIDetector
from app.modules.pii.pii_repository import PiiRepository
from app.extensions.extensions import db


class PIIService:

    @staticmethod
    def scan_text(text):

        user_id = get_jwt_identity()

        detections = PIIDetector.scan_text(text)

        scan = PiiRepository.create_scan(user_id, text)

        for item in detections:
            PiiRepository.add_detection(scan.id, item)

        db.session.commit()

        return {
            "scan_id": scan.id,
            "detections": detections
        }


    @staticmethod
    def enqueue_scan(text):
        user_id = get_jwt_identity()
        scan = PiiRepository.create_scan(user_id, text)
        process_scan.delay(scan.id, text)
        return {"scan_id": scan.id, "status": "queued"}
    
    
    @staticmethod
    def get_user_scans(page, per_page):

        user_id = get_jwt_identity()

        scans = PiiRepository.get_user_scans(
            user_id,
            page,
            per_page
        )

        return {
            "items": [
                {
                    "scan_id": scan.id,
                    "created_at": scan.created_at,
                    "text": scan.input_text
                }
                for scan in scans.items
            ],
            "total": scans.total,
            "page": scans.page,
            "pages": scans.pages
        }
    
    @staticmethod
    def get_scan_results(scan_id):

        user_id = get_jwt_identity()

        scan = PiiRepository.get_scan_by_id(scan_id)

        if scan is None:
            return {"msg": "Scan not found"}, 404

        if scan.user_id != int(user_id):
            return {"msg": "Unauthorized"}, 403

        detections = PiiRepository.get_scan_detections(scan_id)

        return {
            "scan_id": scan.id,
            "created_at": scan.created_at,
            "detections": [
                {
                    "id": d.id,
                    "type": d.pii_type,
                    "value": d.value,
                    "start": d.start_position,
                    "end": d.end_position
                }
                for d in detections
            ]
        }, 200

