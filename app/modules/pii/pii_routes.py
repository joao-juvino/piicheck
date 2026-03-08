# app/modules/pii/pii_routes.py
from flask.views import MethodView
from flask import request
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from app.modules.pii.pii_service import PIIService

pii_blp = Blueprint(
    "pii",
    "pii",
    url_prefix="/pii",
    description="PII scanning endpoints"
)

@pii_blp.route("/scan")
class ScanResource(MethodView):

    @jwt_required()
    def post(self):
        """
        Upload a plain .txt file to enqueue a scan.
        This endpoint accepts multipart/form-data with a 'file' field.
        """
        if "file" not in request.files:
            return {"msg": "File is required"}, 400

        file = request.files["file"]

        if file.filename == "":
            return {"msg": "Empty filename"}, 400

        if not file.filename.lower().endswith(".txt"):
            return {"msg": "Only .txt files are allowed"}, 400

        if file.mimetype != "text/plain":
            return {"msg": "Only text/plain files are allowed"}, 400

        try:
            text = file.read().decode("utf-8")
        except UnicodeDecodeError:
            return {"msg": "File must be valid UTF-8 text"}, 400

        result = PIIService.enqueue_scan(text)
        return result, 202


@pii_blp.route("/scans")
class ScansListResource(MethodView):

    @jwt_required()
    @pii_blp.response(200)
    def get(self):
        """
        List scans of the authenticated user with pagination:
        query params: ?page=1&per_page=10
        """
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        result = PIIService.get_user_scans(page, per_page)
        return result


@pii_blp.route("/scans/<int:scan_id>/results")
class ScanResultsResource(MethodView):

    @jwt_required()
    @pii_blp.response(200)
    def get(self, scan_id):
        """
        Return detections for a single scan (checks ownership).
        """
        return PIIService.get_scan_results(scan_id)