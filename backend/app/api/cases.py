"""Cases API blueprint for the Nyaya Sutra Backend.

Endpoints:
- GET /api/cases/search — Search for a case by court_code and case_number
"""

from flask import Blueprint, g, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from ..middleware.error_handler import ValidationError
from ..services.cache_service import CaseCacheService
from ..services.rate_limiter import RateLimiter
from ..utils.response import success_response

cases_bp = Blueprint("cases", __name__, url_prefix="/api/cases")


@cases_bp.route("/search", methods=["GET"])
@jwt_required()
def search_case():
    """Search for a case by court code and case number.

    Query parameters:
        court_code (required): Court code (e.g., "aft_del", "hc_del")
        case_number (required): Case number to search for

    Requires JWT authentication. Subject to rate limiting based on user tier.
    """
    court_code = request.args.get("court_code", "").strip()
    case_number = request.args.get("case_number", "").strip()

    if not court_code:
        raise ValidationError("court_code query parameter is required.")
    if not case_number:
        raise ValidationError("case_number query parameter is required.")

    # Get user info from JWT
    claims = get_jwt()
    user_id = claims.get("user_id", get_jwt_identity())
    tier = claims.get("tier", "free")

    # Check rate limit
    rate_limiter = RateLimiter()
    rate_limiter.check_limit(user_id, tier)

    # Search case
    service = CaseCacheService()
    result = service.search_case(court_code, case_number)

    # Increment rate limit counter
    rate_limiter.increment(user_id)

    return success_response(result)
