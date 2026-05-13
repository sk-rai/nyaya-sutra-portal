"""Admin API blueprint for the Nyaya Sutra Backend.

Endpoints:
- GET /api/admin/scraper-health — Get scraper health status (admin only)
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from ..extensions import db
from ..middleware.error_handler import TierInsufficientError
from ..utils.response import success_response

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/scraper-health", methods=["GET"])
@jwt_required()
def scraper_health():
    """Get scraper health status for all registered scrapers.

    Requires JWT authentication and admin privileges.
    For now, admin check is based on a special claim in the JWT.
    """
    claims = get_jwt()
    is_admin = claims.get("is_admin", False)

    if not is_admin:
        raise TierInsufficientError(
            "Admin access required to view scraper health."
        )

    # Query scraper health from scraper_registry table
    try:
        result = db.session.execute(
            db.text("SELECT * FROM check_scraper_health()")
        ).fetchall()

        health_data = [
            {
                "court_code": row[0] if len(row) > 0 else None,
                "scraper_key": row[1] if len(row) > 1 else None,
                "is_healthy": row[2] if len(row) > 2 else None,
                "last_success_at": str(row[3]) if len(row) > 3 and row[3] else None,
                "consecutive_failures": row[4] if len(row) > 4 else None,
            }
            for row in result
        ]
    except Exception:
        # If the DB function doesn't exist yet, return empty
        health_data = []

    return success_response(health_data)
