from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from app.modules.pii.pii_schema import (
    FileUploadSchema,
    ScanResponseSchema,
    ScanResultsSchema,
    ScansListSchema,
)
from app.modules.pii.pii_service import PIIService

pii_blp = Blueprint(
    "pii",
    "pii",
    url_prefix="/pii",
    description="Endpoints for scanning and detecting PII (CPF, email, etc)"
)


@pii_blp.route("/scan")
class ScanResource(MethodView):

    @jwt_required()
    @pii_blp.arguments(FileUploadSchema, location="files")
    @pii_blp.response(202, ScanResponseSchema)
    def post(self, files):
        """
        Upload a `.txt` file to enqueue a PII scan.

        The scan is processed asynchronously using Celery.

        Accepted content type:
        - multipart/form-data

        Form fields:
        - file: .txt file containing text to analyze

        Returns:
        - scan_id
        - status (queued)
        """
        
        if "file" not in request.files:
            return {"msg": "File is required"}, 400

        file = files["file"]

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

        return PIIService.enqueue_scan(text)


@pii_blp.route("/scans")
class ScansListResource(MethodView):

    @jwt_required()
    @pii_blp.response(200, ScansListSchema)
    def get(self):
        """
        List scans of the authenticated user.

        Query parameters:
        - page: page number
        - per_page: number of items per page

        Returns paginated scans.
        """

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        return PIIService.get_user_scans(page, per_page)


@pii_blp.route("/scans/<int:scan_id>/results")
class ScanResultsResource(MethodView):

    @jwt_required()
    @pii_blp.response(200, ScanResultsSchema)
    def get(self, scan_id):
        """
        Get PII detections for a specific scan.

        Only the scan owner can access this endpoint.

        Returns:
        - scan metadata
        - list of PII detections
        """

        return PIIService.get_scan_results(scan_id)