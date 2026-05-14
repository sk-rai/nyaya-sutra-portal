"""Tracking API blueprint for the Nyaya Sutra Backend.

Endpoints:
- GET /api/tracking — List tracked cases for the current user
- POST /api/tracking — Track a new case
- DELETE /api/tracking/<case_id> — Untrack a case
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from ..middleware.error_handler import ValidationError
from ..services.cache_service import CaseCacheService
from ..utils.response import success_response

tracking_bp = Blueprint("tracking", __name__, url_prefix="/api/tracking")


@tracking_bp.route("", methods=["GET"])
@jwt_required()
def get_tracked_cases():
    """Get all tracked cases for the current user.

    Requires JWT authentication.
    """
    claims = get_jwt()
    user_id = claims.get("user_id", get_jwt_identity())

    service = CaseCacheService()
    result = service.get_tracked_cases(user_id)

    return success_response(result)


@tracking_bp.route("", methods=["POST"])
@jwt_required()
def track_case():
    """Track a case for the current user.

    Request body:
        {
            "case_id": "uuid-of-case",
            "alert_on_hearing": true,
            "alert_on_status_change": true
        }

    Requires JWT authentication. Subject to tier-based tracking limits.
    """
    data = request.get_json(silent=True)
    if not data:
        raise ValidationError("Request body must be valid JSON.")

    case_id = data.get("case_id", "").strip() if isinstance(data.get("case_id"), str) else str(data.get("case_id", ""))
    if not case_id:
        raise ValidationError("case_id is required.")

    alerts = {
        "alert_on_hearing": data.get("alert_on_hearing", True),
        "alert_on_status_change": data.get("alert_on_status_change", True),
    }

    claims = get_jwt()
    user_id = claims.get("user_id", get_jwt_identity())
    tier = claims.get("tier", "free")

    service = CaseCacheService()
    result = service.track_case(user_id, case_id, alerts)

    return success_response(result, status=201)


@tracking_bp.route("/<case_id>", methods=["DELETE"])
@jwt_required()
def untrack_case(case_id):
    """Untrack a case for the current user.

    Path parameters:
        case_id: UUID of the case to untrack

    Requires JWT authentication.
    """
    claims = get_jwt()
    user_id = claims.get("user_id", get_jwt_identity())

    service = CaseCacheService()
    service.untrack_case(user_id, case_id)

    return success_response({"message": "Case untracked successfully."})
