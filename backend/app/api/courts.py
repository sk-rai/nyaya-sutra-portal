"""Courts API blueprint for the Nyaya Sutra Backend.

Endpoints:
- GET /api/courts — List all active courts with optional type filter
"""

from flask import Blueprint, request

from ..extensions import db
from ..models.court import Court
from ..utils.response import success_response

courts_bp = Blueprint("courts", __name__, url_prefix="/api/courts")


@courts_bp.route("", methods=["GET"])
def list_courts():
    """List all active courts.

    Query parameters:
        court_type (optional): Filter by court type (e.g., "aft", "cat", "hc", "sc")

    Returns:
        List of courts sorted by court_type then alphabetically by short_name.
        No authentication required.
    """
    court_type = request.args.get("court_type", "").strip().lower()

    query = Court.query.filter_by(is_active=True)

    if court_type:
        query = query.filter(db.func.lower(Court.court_type) == court_type)

    courts = query.order_by(Court.court_type, Court.short_name).all()

    result = [court.to_dict() for court in courts]

    return success_response(result)
