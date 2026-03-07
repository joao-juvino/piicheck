from app.extensions.celery_app import celery
from app.extensions.extensions import db
from app.modules.pii.pii_detector import PIIDetector
from app.modules.pii.pii_repository import PiiRepository
from app.modules.pii.pii_scan_model import PiiScan

from app.extensions.celery_app import celery

@celery.task
def process_scan(scan_id, text):

    scan = PiiScan.query.get(scan_id)

    if not scan:
        return {"error": f"scan {scan_id} not found"}

    scan.status = "processing"
    db.session.commit()

    detections = PIIDetector.scan_text(text)

    for item in detections:
        PiiRepository.add_detection(scan_id, item)

    scan.status = "done"
    db.session.commit()