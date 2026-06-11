"""Admin API blueprint for the Nyaya Sutra Backend.

Endpoints:
- GET /api/admin/scraper-health — Get scraper health status
- GET /api/admin/stats — Get platform statistics (users, tiers, etc.)
- GET /api/admin/users — List all users with tier info
- POST /api/admin/upload-causelist — Upload and parse a cause list PDF
"""

import logging
from datetime import datetime, timezone

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import func

from ..extensions import db
from ..middleware.error_handler import TierInsufficientError, ValidationError
from ..models.user import User, UserSession
from ..models.subscription import Subscription
from ..models.case import CaseCache
from ..models.tracking import UserTrackedCase
from ..utils.response import success_response

logger = logging.getLogger(__name__)

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


@admin_bp.route("/upload-causelist", methods=["POST"])
@jwt_required()
def upload_causelist():
    """Upload a cause list PDF for parsing and database seeding.

    Accepts a PDF file upload + court_code parameter.
    Parses the PDF using the AFT/CAT parser and stores all cases in the DB.
    Checks file hash to prevent duplicate processing.

    Any logged-in user can upload (not restricted to admin).

    Form data:
        file: PDF file (multipart/form-data)
        court_code: Court code (e.g., 'aft_del', 'cat_del')
        hearing_date: Optional hearing date (YYYY-MM-DD) for the cause list

    Returns:
        Summary of parsed and stored cases.
    """
    import hashlib
    from flask_jwt_extended import get_jwt_identity

    # Validate file upload
    if "file" not in request.files:
        raise ValidationError("No file uploaded. Please attach a PDF file.")

    file = request.files["file"]
    if not file.filename:
        raise ValidationError("No file selected.")

    if not file.filename.lower().endswith(".pdf"):
        raise ValidationError("Only PDF files are accepted.")

    court_code = request.form.get("court_code", "").strip()
    if not court_code:
        raise ValidationError("court_code is required.")

    hearing_date_str = request.form.get("hearing_date", "").strip()

    # Read the PDF content
    pdf_content = file.read()
    if not pdf_content:
        raise ValidationError("Uploaded file is empty.")

    if pdf_content[:4] != b"%PDF":
        raise ValidationError("Uploaded file is not a valid PDF.")

    # Calculate file hash for duplicate detection
    file_hash = hashlib.sha256(pdf_content).hexdigest()

    # Check if this file was already processed
    existing_upload = db.session.execute(
        db.text("SELECT id, cases_parsed, created_at FROM upload_log WHERE file_hash = :hash"),
        {"hash": file_hash}
    ).fetchone()

    if existing_upload:
        return success_response({
            "message": "This file has already been processed.",
            "status": "duplicate",
            "filename": file.filename,
            "court_code": court_code,
            "cases_found": existing_upload[1] if existing_upload[1] else 0,
            "uploaded_at": str(existing_upload[2]) if existing_upload[2] else None,
        })

    logger.info(
        f"[upload] Processing cause list PDF for {court_code} "
        f"({len(pdf_content)} bytes, filename={file.filename}, hash={file_hash[:12]}...)"
    )

    # Get the appropriate parser
    from ..scrapers.registry import ScraperFactory

    factory = ScraperFactory()
    scraper = factory.get_scraper(court_code)

    if not scraper:
        raise ValidationError(f"No parser available for court: {court_code}")

    # Parse the PDF
    results = scraper.parse(pdf_content)

    if not results:
        # Log failed upload
        self._log_upload(file_hash, file.filename, court_code, hearing_date_str,
                        len(pdf_content), 0, 0, 0, "failed", "No cases found in PDF")
        return success_response({
            "message": "PDF parsed but no cases found. Check the PDF format.",
            "status": "no_cases",
            "cases_found": 0,
            "cases_new": 0,
        })

    # Store parsed cases in the database
    stored = 0
    updated = 0
    errors = 0

    for scrape_result in results:
        structured = scrape_result.structured
        case_number = structured.get("case_number", "").strip()

        if not case_number:
            errors += 1
            continue

        try:
            # Check if case already exists
            existing = CaseCache.query.filter_by(
                court_code=court_code,
                case_number=case_number,
            ).first()

            if existing:
                # Update existing record
                existing.petitioner = structured.get("petitioner") or existing.petitioner
                existing.respondent = structured.get("respondent") or existing.respondent
                existing.advocate_petitioner = structured.get("advocate_petitioner") or existing.advocate_petitioner
                existing.advocate_respondent = structured.get("advocate_respondent") or existing.advocate_respondent
                existing.bench = structured.get("bench") or existing.bench
                existing.item_number = structured.get("item_number") or existing.item_number
                existing.case_title = structured.get("case_title") or existing.case_title
                existing.raw_scraped_data = {"raw": scrape_result.raw_data, "source": file.filename}
                existing.parse_confidence = scrape_result.confidence
                existing.fetched_at = datetime.now(timezone.utc)
                existing.last_refreshed_at = datetime.now(timezone.utc)
                existing.scraper_version = scraper.SCRAPER_VERSION
                if hearing_date_str:
                    try:
                        existing.next_hearing_date = datetime.strptime(hearing_date_str, "%Y-%m-%d").date()
                    except ValueError:
                        pass
                updated += 1
            else:
                # Create new case
                case_obj = CaseCache(
                    court_code=court_code,
                    case_number=case_number,
                    case_title=structured.get("case_title", ""),
                    petitioner=structured.get("petitioner", ""),
                    respondent=structured.get("respondent", ""),
                    advocate_petitioner=structured.get("advocate_petitioner", ""),
                    advocate_respondent=structured.get("advocate_respondent", ""),
                    bench=structured.get("bench", ""),
                    item_number=structured.get("item_number", ""),
                    case_status="pending",
                    parse_confidence=scrape_result.confidence,
                    raw_scraped_data={"raw": scrape_result.raw_data, "source": file.filename},
                    extra_fields=scrape_result.extra_fields,
                    source_url=f"upload:{file.filename}",
                    scraper_version=scraper.SCRAPER_VERSION,
                    fetched_at=datetime.now(timezone.utc),
                )
                if hearing_date_str:
                    try:
                        case_obj.next_hearing_date = datetime.strptime(hearing_date_str, "%Y-%m-%d").date()
                    except ValueError:
                        pass
                db.session.add(case_obj)
                stored += 1

        except Exception as e:
            logger.error(f"[upload] Error storing case {case_number}: {e}")
            errors += 1

    # Log the upload
    try:
        user_id = get_jwt_identity()
        db.session.execute(
            db.text("""
                INSERT INTO upload_log (file_hash, filename, court_code, hearing_date,
                    file_size_bytes, cases_parsed, cases_new, cases_updated, uploaded_by, status)
                VALUES (:hash, :filename, :court_code, :hearing_date,
                    :file_size, :cases_parsed, :cases_new, :cases_updated, :user_id, 'success')
            """),
            {
                "hash": file_hash,
                "filename": file.filename,
                "court_code": court_code,
                "hearing_date": hearing_date_str or None,
                "file_size": len(pdf_content),
                "cases_parsed": len(results),
                "cases_new": stored,
                "cases_updated": updated,
                "user_id": user_id,
            }
        )
    except Exception as e:
        # upload_log table might not exist yet — non-fatal
        logger.warning(f"[upload] Could not log upload: {e}")

    db.session.commit()

    logger.info(
        f"[upload] Complete for {court_code}: "
        f"parsed={len(results)}, stored={stored}, updated={updated}, errors={errors}"
    )

    return success_response({
        "message": f"Cause list processed successfully for {court_code}.",
        "status": "success",
        "filename": file.filename,
        "court_code": court_code,
        "hearing_date": hearing_date_str or None,
        "cases_found": len(results),
        "cases_new": stored,
        "cases_updated": updated,
        "errors": errors,
    })
