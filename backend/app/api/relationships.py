"""Relationships API blueprint for the Nyaya Sutra Backend.

Endpoints:
- POST /api/cases/relationships — Create a case relationship
- GET /api/cases/<case_id>/relationships — Get all related cases
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from ..middleware.error_handler import ValidationError
from ..services.cache_service import CaseCacheService
from ..utils.response import success_response

relationships_bp = Blueprint("relationships", __name__, url_prefix="/api/cases")


@relationships_bp.route("/relationships", methods=["POST"])
@jwt_required()
def create_relationship():
    """Create a relationship between two cases.

    Request body:
        {
            "case_id": "uuid-of-case",
            "related_case_id": "uuid-of-related-case",
            "relationship_type": "appeal" | "review" | "transfer" | "connected" | "cited_in" | "overruled_by"
        }

    The relationship is always set with detected_by="user" and confidence=1.0.
    Duplicate relationships (same case_id, related_case_id, type) are rejected.

    Requires JWT authentication.
    """
    data = request.get_json(silent=True)
    if not data:
        raise ValidationError("Request body must be valid JSON.")

    case_id = data.get("case_id", "").strip() if isinstance(data.get("case_id"), str) else str(data.get("case_id", ""))
    related_case_id = data.get("related_case_id", "").strip() if isinstance(data.get("related_case_id"), str) else str(data.get("related_case_id", ""))
    relationship_type = data.get("relationship_type", "").strip()

    if not case_id:
        raise ValidationError("case_id is required.")
    if not related_case_id:
        raise ValidationError("related_case_id is required.")
    if not relationship_type:
        raise ValidationError("relationship_type is required.")

    service = CaseCacheService()
    result = service.link_cases(case_id, related_case_id, relationship_type)

    return success_response(result, status=201)


@relationships_bp.route("/<case_id>/relationships", methods=["GET"])
@jwt_required()
def get_relationships(case_id):
    """Get all related cases for a given case (both directions).

    Path parameters:
        case_id: UUID of the case

    Requires JWT authentication.
    """
    service = CaseCacheService()
    result = service.get_related_cases(case_id)

    return success_response(result)
