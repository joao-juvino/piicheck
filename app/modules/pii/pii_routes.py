from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.modules.pii.pii_service import PIIService
from app.modules.pii.pii_schema import PiiScanSchema


pii_bp = Blueprint("pii", __name__)

schema = PiiScanSchema()


@pii_bp.route("/scan", methods=["POST"])
@jwt_required()
def scan():

    data = schema.load(request.json)

    result = PIIService.scan_text(data["text"])

    return result, 200


@pii_bp.route("/scans", methods=["GET"])
@jwt_required()
def get_scans():

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    result = PIIService.get_user_scans(page, per_page)

    return result, 200

@pii_bp.route("/scans/<int:scan_id>/results", methods=["GET"])
@jwt_required()
def get_scan_results(scan_id):

    return PIIService.get_scan_results(scan_id)

