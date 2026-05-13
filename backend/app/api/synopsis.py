"""Synopsis API blueprint for the Nyaya Sutra Backend.

Endpoints:
- GET /api/synopsis/<case_id> — Get AI-generated case synopsis (advocate_premium only)
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from ..middleware.error_handler import TierInsufficientError, NotFoundError
from ..utils.response import success_response

synopsis_bp = Blueprint("synopsis", __name__, url_prefix="/api/synopsis")


@synopsis_bp.route("/<case_id>", methods=["GET"])
@jwt_required()
def get_synopsis(case_id):
    """Get AI-generated synopsis for a case.

    Path parameters:
        case_id: UUID of the case

    Requires JWT authentication and advocate_premium tier.
    Returns 403 for users on other tiers.
    """
    claims = get_jwt()
    tier = claims.get("tier", "free")

    if tier != "advocate_premium":
        raise TierInsufficientError(
            "Case synopsis is available only for Advocate Premium subscribers."
        )

    # Placeholder implementation — will be replaced with actual AI synopsis generation
    synopsis_data = {
        "case_id": case_id,
        "synopsis": None,
        "status": "not_available",
        "message": "Synopsis generation is not yet implemented. This feature will be available in a future release.",
    }

    return success_response(synopsis_data)
