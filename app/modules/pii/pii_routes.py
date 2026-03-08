from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.modules.pii.pii_service import PIIService

pii_bp = Blueprint("pii", __name__)


@pii_bp.route("/scan", methods=["POST"])
@jwt_required()
def scan():

    if "file" not in request.files:
        return {"msg": "File is required"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"msg": "Empty filename"}, 400

    if not file.filename.endswith(".txt"):
        return {"msg": "Only .txt files are allowed"}, 400

    if file.mimetype != "text/plain":
        return {"msg": "Only text/plain files are allowed"}, 400

    try:
        text = file.read().decode("utf-8")
    except UnicodeDecodeError:
        return {"msg": "File must be valid UTF-8 text"}, 400

    result = PIIService.enqueue_scan(text)

    return result, 202


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

