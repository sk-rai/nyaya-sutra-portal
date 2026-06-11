"""Case cache service for the Nyaya Sutra Backend API.

Handles case search with caching, case tracking (add/remove),
tracked case retrieval, and case relationship management.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from flask import current_app

from ..extensions import db
from ..middleware.error_handler import NotFoundError, ValidationError
from ..models.case import CaseCache, CaseRelationship
from ..models.tracking import UserTrackedCase
from ..models.user import User

logger = logging.getLogger(__name__)


class CaseCacheService:
    """Service handling case cache operations, tracking, and relationships."""

    def search_case(self, court_code: str, case_number: str, user_id: str = None) -> dict:
        """Check cache for a case, return data with freshness indicator.

        Flow:
        - Query case_cache for matching court_code + case_number
        - If found and fresh (<24h for untracked): return cached data, update last_accessed_at
        - If found but stale (>24h, untracked): return stale data with freshness indicator
          (scraper integration pending)
        - If not found: return error (scraper integration pending)

        Args:
            court_code: The court code (e.g., 'aft_del').
            case_number: The case number string.
            user_id: Optional user ID for context.

        Returns:
            Dict with case data and freshness indicator.

        Raises:
            NotFoundError: If case is not in cache (scraper not yet integrated).
        """
        case = CaseCache.query.filter_by(
            court_code=court_code,
            case_number=case_number,
        ).first()

        if case:
            # Update last_accessed_at
            case.last_accessed_at = datetime.now(timezone.utc)
            db.session.commit()

            freshness = self.get_freshness(case.fetched_at)

            result = case.to_dict()
            result["freshness"] = freshness
            return result

        # Case not in cache — trigger scraper to fetch from court website
        result = self._scrape_and_cache(court_code, case_number)
        if result:
            return result

        raise NotFoundError(
            f"Case {case_number} not found in {court_code} cause list."
        )

    def _scrape_and_cache(self, court_code: str, case_number: str) -> Optional[dict]:
        """Trigger scraper to fetch case from court website and cache it.

        Downloads the cause list PDF, parses ALL cases from it,
        stores them in cache, and returns the matching case.

        Args:
            court_code: Court code (e.g., 'aft_del').
            case_number: Case number to search for.

        Returns:
            Dict with case data if found, None otherwise.
        """
        from ..scrapers.registry import ScraperFactory

        factory = ScraperFactory()
        scraper = factory.get_scraper(court_code.replace("_", "_"))

        if not scraper:
            logger.warning(f"No scraper available for court: {court_code}")
            return None

        try:
            # Fetch and parse the PDF
            raw_content = scraper.fetch_pdf(court_code, case_number)
            if not raw_content:
                logger.info(f"No PDF content fetched for {court_code}")
                return None

            results = scraper.parse(raw_content)
            if not results:
                logger.info(f"No cases parsed from {court_code} PDF")
                return None

            logger.info(f"Parsed {len(results)} cases from {court_code} cause list")

            # Store ALL parsed cases in cache (benefits future searches)
            matched_case = None
            case_number_normalized = case_number.strip().lower().replace(" ", "")

            for scrape_result in results:
                structured = scrape_result.structured
                scraped_case_number = structured.get("case_number", "")

                if not scraped_case_number:
                    continue

                # Check if this case already exists in cache
                existing = CaseCache.query.filter_by(
                    court_code=court_code,
                    case_number=scraped_case_number,
                ).first()

                if existing:
                    # Update existing cache entry
                    existing.petitioner = structured.get("petitioner") or existing.petitioner
                    existing.respondent = structured.get("respondent") or existing.respondent
                    existing.advocate_petitioner = structured.get("advocate_petitioner") or existing.advocate_petitioner
                    existing.advocate_respondent = structured.get("advocate_respondent") or existing.advocate_respondent
                    existing.bench = structured.get("bench") or existing.bench
                    existing.item_number = structured.get("item_number") or existing.item_number
                    existing.case_title = structured.get("case_title") or existing.case_title
                    existing.raw_scraped_data = {"raw": scrape_result.raw_data}
                    existing.parse_confidence = scrape_result.confidence
                    existing.fetched_at = datetime.now(timezone.utc)
                    existing.last_refreshed_at = datetime.now(timezone.utc)
                    existing.scraper_version = scraper.SCRAPER_VERSION

                    case_obj = existing
                else:
                    # Create new cache entry
                    case_obj = CaseCache(
                        court_code=court_code,
                        case_number=scraped_case_number,
                        case_title=structured.get("case_title", ""),
                        petitioner=structured.get("petitioner", ""),
                        respondent=structured.get("respondent", ""),
                        advocate_petitioner=structured.get("advocate_petitioner", ""),
                        advocate_respondent=structured.get("advocate_respondent", ""),
                        bench=structured.get("bench", ""),
                        item_number=structured.get("item_number", ""),
                        case_status="pending",
                        parse_confidence=scrape_result.confidence,
                        raw_scraped_data={"raw": scrape_result.raw_data},
                        extra_fields=scrape_result.extra_fields,
                        source_url=scrape_result.source_url,
                        scraper_version=scraper.SCRAPER_VERSION,
                        fetched_at=datetime.now(timezone.utc),
                    )
                    db.session.add(case_obj)

                # Check if this is our target case
                scraped_normalized = scraped_case_number.strip().lower().replace(" ", "")
                if scraped_normalized == case_number_normalized:
                    matched_case = case_obj

            db.session.commit()

            if matched_case:
                result = matched_case.to_dict()
                result["freshness"] = "fresh"
                return result

            # Fuzzy match if exact match failed
            for scrape_result in results:
                scraped_num = scrape_result.structured.get("case_number", "").strip().lower().replace(" ", "")
                if case_number_normalized in scraped_num or scraped_num in case_number_normalized:
                    # Find the cached version
                    case_obj = CaseCache.query.filter_by(
                        court_code=court_code,
                        case_number=scrape_result.structured.get("case_number"),
                    ).first()
                    if case_obj:
                        result = case_obj.to_dict()
                        result["freshness"] = "fresh"
                        return result

            return None

        except Exception as e:
            logger.error(f"Scraper failed for {court_code}/{case_number}: {e}", exc_info=True)
            db.session.rollback()
            return None

    def get_freshness(self, fetched_at: datetime) -> str:
        """Calculate freshness indicator based on fetched_at timestamp.

        Args:
            fetched_at: The datetime when the case was last fetched.

        Returns:
            'fresh' (<6h), 'recent' (<24h), 'stale' (<48h), 'very_stale' (>48h).
        """
        if not fetched_at:
            return "very_stale"

        now = datetime.now(timezone.utc)
        # Ensure fetched_at is timezone-aware
        if fetched_at.tzinfo is None:
            fetched_at = fetched_at.replace(tzinfo=timezone.utc)

        age = now - fetched_at

        if age < timedelta(hours=6):
            return "fresh"
        elif age < timedelta(hours=24):
            return "recent"
        elif age < timedelta(hours=48):
            return "stale"
        else:
            return "very_stale"

    def track_case(self, user_id: str, case_id: str, alerts: dict = None) -> dict:
        """Add a case to the user's tracked list with alert preferences.

        Checks the user's tier limit before adding.

        Args:
            user_id: The user's UUID string.
            case_id: The case UUID string.
            alerts: Optional dict with alert preferences
                    (alert_sms, alert_whatsapp, alert_email, notes).

        Returns:
            Dict with the created tracking record.

        Raises:
            ValidationError: If tier limit is exceeded or case already tracked.
            NotFoundError: If user or case not found.
        """
        import uuid as uuid_mod

        # Parse UUIDs
        try:
            uid = uuid_mod.UUID(user_id) if isinstance(user_id, str) else user_id
            cid = uuid_mod.UUID(case_id) if isinstance(case_id, str) else case_id
        except (ValueError, AttributeError):
            raise ValidationError("Invalid user_id or case_id format.")

        # Verify user exists
        user = db.session.get(User, uid)
        if not user:
            raise NotFoundError("User not found.")

        # Verify case exists
        case = db.session.get(CaseCache, cid)
        if not case:
            raise NotFoundError("Case not found.")

        # Check if already tracked
        existing = UserTrackedCase.query.filter_by(
            user_id=uid, case_id=cid
        ).first()
        if existing:
            raise ValidationError("Case is already being tracked by this user.")

        # Check tier limit
        tier_config = current_app.config.get("TIER_CONFIG", {})
        user_tier_config = tier_config.get(user.tier, {})
        max_tracked = user_tier_config.get("max_tracked_cases", 5)

        current_count = UserTrackedCase.query.filter_by(user_id=uid).count()
        if current_count >= max_tracked:
            raise ValidationError(
                f"Tracking limit reached. Your '{user.tier}' tier allows "
                f"a maximum of {max_tracked} tracked cases.",
                details={"limit": max_tracked, "current": current_count, "tier": user.tier},
            )

        # Create tracking record
        alerts = alerts or {}
        tracked = UserTrackedCase(
            user_id=uid,
            case_id=cid,
            alert_enabled=alerts.get("alert_enabled", True),
            alert_sms=alerts.get("alert_sms", False),
            alert_whatsapp=alerts.get("alert_whatsapp", False),
            alert_email=alerts.get("alert_email", True),
            notes=alerts.get("notes"),
        )

        db.session.add(tracked)

        # Update case tracking fields (in case DB triggers aren't available)
        case.is_tracked = True
        case.tracked_by_count = (case.tracked_by_count or 0) + 1

        db.session.commit()

        return tracked.to_dict()

    def untrack_case(self, user_id: str, case_id: str) -> None:
        """Remove a case from the user's tracked list.

        Args:
            user_id: The user's UUID string.
            case_id: The case UUID string.

        Raises:
            NotFoundError: If the tracking record doesn't exist.
        """
        import uuid as uuid_mod

        try:
            uid = uuid_mod.UUID(user_id) if isinstance(user_id, str) else user_id
            cid = uuid_mod.UUID(case_id) if isinstance(case_id, str) else case_id
        except (ValueError, AttributeError):
            raise NotFoundError("Tracking record not found.")

        tracked = UserTrackedCase.query.filter_by(
            user_id=uid, case_id=cid
        ).first()

        if not tracked:
            raise NotFoundError("Tracking record not found.")

        # Update case tracking fields (in case DB triggers aren't available)
        case = db.session.get(CaseCache, cid)
        if case:
            case.tracked_by_count = max((case.tracked_by_count or 1) - 1, 0)
            if case.tracked_by_count == 0:
                case.is_tracked = False

        db.session.delete(tracked)
        db.session.commit()

    def get_tracked_cases(self, user_id: str) -> list:
        """Return all tracked cases for a user with details and freshness.

        Args:
            user_id: The user's UUID string.

        Returns:
            List of dicts with case data and freshness indicators.
        """
        import uuid as uuid_mod

        try:
            uid = uuid_mod.UUID(user_id) if isinstance(user_id, str) else user_id
        except (ValueError, AttributeError):
            return []

        tracked_records = (
            UserTrackedCase.query
            .filter_by(user_id=uid)
            .all()
        )

        results = []
        for record in tracked_records:
            case = db.session.get(CaseCache, record.case_id)
            if case:
                case_data = case.to_dict()
                case_data["freshness"] = self.get_freshness(case.fetched_at)
                case_data["tracking"] = record.to_dict()
                results.append(case_data)

        return results

    def link_cases(self, case_id: str, related_id: str, rel_type: str) -> dict:
        """Create a case relationship record.

        Args:
            case_id: The source case UUID string.
            related_id: The related case UUID string.
            rel_type: Relationship type (one of 6 valid types).

        Returns:
            Dict with the created relationship record.

        Raises:
            ValidationError: If relationship type is invalid or duplicate exists.
            NotFoundError: If either case is not found.
        """
        import uuid as uuid_mod

        # Validate relationship type
        if rel_type not in CaseRelationship.RELATIONSHIP_TYPES:
            raise ValidationError(
                f"Invalid relationship type '{rel_type}'. "
                f"Must be one of: {', '.join(CaseRelationship.RELATIONSHIP_TYPES)}",
            )

        # Parse UUIDs
        try:
            cid = uuid_mod.UUID(case_id) if isinstance(case_id, str) else case_id
            rid = uuid_mod.UUID(related_id) if isinstance(related_id, str) else related_id
        except (ValueError, AttributeError):
            raise ValidationError("Invalid case_id or related_case_id format.")

        # Verify both cases exist
        case = db.session.get(CaseCache, cid)
        if not case:
            raise NotFoundError("Source case not found.")

        related_case = db.session.get(CaseCache, rid)
        if not related_case:
            raise NotFoundError("Related case not found.")

        # Check for duplicate
        existing = CaseRelationship.query.filter_by(
            case_id=cid,
            related_case_id=rid,
            relationship_type=rel_type,
        ).first()
        if existing:
            raise ValidationError(
                "This relationship already exists between these cases."
            )

        # Create relationship
        relationship = CaseRelationship(
            case_id=cid,
            related_case_id=rid,
            relationship_type=rel_type,
            detected_by="user",
            confidence=1.0,
        )

        db.session.add(relationship)
        db.session.commit()

        return relationship.to_dict()

    def get_related_cases(self, case_id: str) -> list:
        """Return all related cases for a given case (both directions).

        Queries relationships where the case appears as either
        case_id or related_case_id.

        Args:
            case_id: The case UUID string.

        Returns:
            List of relationship dicts.
        """
        import uuid as uuid_mod

        try:
            cid = uuid_mod.UUID(case_id) if isinstance(case_id, str) else case_id
        except (ValueError, AttributeError):
            return []

        # Query both directions
        as_source = CaseRelationship.query.filter_by(case_id=cid).all()
        as_related = CaseRelationship.query.filter_by(related_case_id=cid).all()

        results = []
        for rel in as_source:
            data = rel.to_dict()
            data["direction"] = "outgoing"
            results.append(data)

        for rel in as_related:
            data = rel.to_dict()
            data["direction"] = "incoming"
            results.append(data)

        return results
