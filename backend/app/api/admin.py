"""Admin API blueprint for the Nyaya Sutra Backend.

Endpoints:
- GET /api/admin/scraper-health — Get scraper health status
- GET /api/admin/stats — Get platform statistics (users, tiers, etc.)
- GET /api/admin/users — List all users with tier info
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import func

from ..extensions import db
from ..middleware.error_handler import TierInsufficientError
from ..models.user import User, UserSession
from ..models.subscription import Subscription
from ..models.case import CaseCache
from ..models.tracking import UserTrackedCase
from ..utils.response import success_response

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def require_admin():
    """Check if current user has admin privileges."""
    claims = get_jwt()
    if not claims.get("is_admin", False):
        raise TierInsufficientError("Admin access required.")


@admin_bp.route("/scraper-health", methods=["GET"])
@jwt_required()
def scraper_health():
    """Get scraper health status for all registered scrapers."""
    require_admin()

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
        health_data = []

    return success_response(health_data)


@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
def platform_stats():
    """Get platform-wide statistics.

    Returns user counts by tier, active sessions, tracked cases, etc.
    """
    require_admin()

    # User counts by tier
    tier_counts = db.session.query(
        User.tier, func.count(User.id)
    ).group_by(User.tier).all()

    tier_stats = {tier: count for tier, count in tier_counts}

    # User counts by type
    type_counts = db.session.query(
        User.user_type, func.count(User.id)
    ).group_by(User.user_type).all()

    type_stats = {utype: count for utype, count in type_counts}

    # Total users
    total_users = db.session.query(func.count(User.id)).scalar() or 0

    # Verified vs unverified
    verified_count = db.session.query(func.count(User.id)).filter(
        User.is_verified == True
    ).scalar() or 0

    # Active sessions (not revoked, not expired)
    active_sessions = db.session.query(func.count(UserSession.id)).filter(
        UserSession.revoked_at.is_(None)
    ).scalar() or 0

    # Total tracked cases
    total_tracked = db.session.query(func.count(UserTrackedCase.id)).scalar() or 0

    # Cached cases
    total_cached = db.session.query(func.count(CaseCache.id)).scalar() or 0

    # Active subscriptions
    active_subs = db.session.query(func.count(Subscription.id)).filter(
        Subscription.status == "active"
    ).scalar() or 0

    stats = {
        "users": {
            "total": total_users,
            "verified": verified_count,
            "unverified": total_users - verified_count,
            "by_tier": tier_stats,
            "by_type": type_stats,
        },
        "sessions": {
            "active": active_sessions,
        },
        "cases": {
            "tracked": total_tracked,
            "cached": total_cached,
        },
        "subscriptions": {
            "active": active_subs,
        },
    }

    return success_response(stats)


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    """List all users with pagination.

    Query params:
        page (int): Page number (default 1)
        per_page (int): Items per page (default 20, max 100)
        tier (str): Filter by tier
        user_type (str): Filter by user_type
    """
    require_admin()

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    tier_filter = request.args.get("tier", "").strip()
    type_filter = request.args.get("user_type", "").strip()

    query = User.query

    if tier_filter:
        query = query.filter(User.tier == tier_filter)
    if type_filter:
        query = query.filter(User.user_type == type_filter)

    query = query.order_by(User.created_at.desc())

    # Paginate
    total = query.count()
    users = query.offset((page - 1) * per_page).limit(per_page).all()

    return success_response({
        "users": [u.to_dict(include_private=True) for u in users],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
        },
    })
