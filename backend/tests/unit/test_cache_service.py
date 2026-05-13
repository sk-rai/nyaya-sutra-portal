"""Unit tests for CaseCacheService."""

import uuid
from datetime import datetime, timedelta, timezone

import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def app(monkeypatch):
    """Create a test Flask app with in-memory SQLite for unit tests."""
    monkeypatch.setenv("TEST_DATABASE_URL", "sqlite:///:memory:")

    from sqlalchemy.dialects.sqlite.base import SQLiteTypeCompiler

    if not hasattr(SQLiteTypeCompiler, "visit_UUID"):
        SQLiteTypeCompiler.visit_UUID = lambda self, type_, **kw: "CHAR(36)"
    if not hasattr(SQLiteTypeCompiler, "visit_ARRAY"):
        SQLiteTypeCompiler.visit_ARRAY = lambda self, type_, **kw: "TEXT"
    if not hasattr(SQLiteTypeCompiler, "visit_JSONB"):
        SQLiteTypeCompiler.visit_JSONB = lambda self, type_, **kw: "TEXT"
    if not hasattr(SQLiteTypeCompiler, "visit_JSON"):
        SQLiteTypeCompiler.visit_JSON = lambda self, type_, **kw: "TEXT"

    from app import create_app
    from app.extensions import db

    app = create_app("testing")
    # Override DB URI directly in case config was already cached
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        import uuid as uuid_mod

        for table in db.metadata.tables.values():
            for column in table.columns:
                if column.server_default is not None:
                    sd_text = str(column.server_default.arg)
                    if "uuid_generate_v4" in sd_text or "::" in sd_text:
                        column.server_default = None
                        if column.primary_key and "UUID" in str(type(column.type).__name__).upper():
                            column.default = db.ColumnDefault(uuid_mod.uuid4)

        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def service(app):
    """CaseCacheService instance within app context."""
    from app.services.cache_service import CaseCacheService

    with app.app_context():
        yield CaseCacheService()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    from app.extensions import db
    from app.models.user import User

    with app.app_context():
        user = User(
            name="Test User",
            email="test@example.com",
            phone="9876543210",
            user_type="individual",
            tier="free",
            is_verified=True,
        )
        db.session.add(user)
        db.session.commit()
        yield user


@pytest.fixture
def sample_court(app):
    """Create a sample court for testing."""
    from app.extensions import db
    from app.models.court import Court

    with app.app_context():
        court = Court(
            code="aft_del",
            name="Armed Forces Tribunal Delhi",
            short_name="AFT Delhi",
            court_type="aft",
            state="Delhi",
            city="New Delhi",
            is_active=True,
        )
        db.session.add(court)
        db.session.commit()
        yield court


@pytest.fixture
def sample_case(app, sample_court):
    """Create a sample case in the cache."""
    from app.extensions import db
    from app.models.case import CaseCache

    with app.app_context():
        case = CaseCache(
            court_code="aft_del",
            case_number="OA/123/2024",
            case_title="Test vs Union of India",
            petitioner="Test Petitioner",
            respondent="Union of India",
            fetched_at=datetime.now(timezone.utc) - timedelta(hours=2),
            last_accessed_at=datetime.now(timezone.utc) - timedelta(hours=2),
            is_tracked=False,
            tracked_by_count=0,
        )
        db.session.add(case)
        db.session.commit()
        yield case


# ---------------------------------------------------------------------------
# search_case Tests
# ---------------------------------------------------------------------------


class TestSearchCase:
    """Tests for CaseCacheService.search_case."""

    def test_search_case_cache_hit(self, app, service, sample_case):
        """Cache hit should return case data with freshness."""
        with app.app_context():
            result = service.search_case("aft_del", "OA/123/2024")

            assert result["court_code"] == "aft_del"
            assert result["case_number"] == "OA/123/2024"
            assert result["case_title"] == "Test vs Union of India"
            assert result["freshness"] == "fresh"

    def test_search_case_updates_last_accessed(self, app, service, sample_case):
        """Cache hit should update last_accessed_at."""
        from app.extensions import db
        from app.models.case import CaseCache

        with app.app_context():
            old_accessed = sample_case.last_accessed_at
            service.search_case("aft_del", "OA/123/2024")

            # Re-query to get updated value
            case = CaseCache.query.filter_by(case_number="OA/123/2024").first()
            assert case.last_accessed_at > old_accessed

    def test_search_case_not_found_raises_error(self, app, service, sample_court):
        """Cache miss should raise NotFoundError."""
        from app.middleware.error_handler import NotFoundError

        with app.app_context():
            with pytest.raises(NotFoundError):
                service.search_case("aft_del", "NONEXISTENT/999/2024")


# ---------------------------------------------------------------------------
# track_case Tests
# ---------------------------------------------------------------------------


class TestTrackCase:
    """Tests for CaseCacheService.track_case."""

    def test_track_case_success(self, app, service, sample_user, sample_case):
        """Tracking a case should create a UserTrackedCase record."""
        with app.app_context():
            result = service.track_case(
                str(sample_user.id),
                str(sample_case.id),
                alerts={"alert_email": True, "alert_sms": False},
            )

            assert result["user_id"] == str(sample_user.id)
            assert result["case_id"] == str(sample_case.id)
            assert result["alert_email"] is True
            assert result["alert_sms"] is False

    def test_track_case_tier_limit_exceeded(self, app, service, sample_user, sample_court):
        """Exceeding tier limit should raise ValidationError."""
        from app.extensions import db
        from app.middleware.error_handler import ValidationError
        from app.models.case import CaseCache

        with app.app_context():
            # Free tier allows 5 tracked cases. Create 5 cases and track them.
            for i in range(5):
                case = CaseCache(
                    court_code="aft_del",
                    case_number=f"OA/{i}/2024",
                    case_title=f"Case {i}",
                    fetched_at=datetime.now(timezone.utc),
                    last_accessed_at=datetime.now(timezone.utc),
                    is_tracked=False,
                    tracked_by_count=0,
                )
                db.session.add(case)
            db.session.commit()

            cases = CaseCache.query.filter(
                CaseCache.case_number.like("OA/%/2024")
            ).all()

            for case in cases[:5]:
                service.track_case(str(sample_user.id), str(case.id))

            # Now create a 6th case and try to track it
            extra_case = CaseCache(
                court_code="aft_del",
                case_number="OA/999/2024",
                case_title="Extra Case",
                fetched_at=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
                is_tracked=False,
                tracked_by_count=0,
            )
            db.session.add(extra_case)
            db.session.commit()

            with pytest.raises(ValidationError, match="Tracking limit reached"):
                service.track_case(str(sample_user.id), str(extra_case.id))


# ---------------------------------------------------------------------------
# untrack_case Tests
# ---------------------------------------------------------------------------


class TestUntrackCase:
    """Tests for CaseCacheService.untrack_case."""

    def test_untrack_case_success(self, app, service, sample_user, sample_case):
        """Untracking should remove the tracking record."""
        from app.models.tracking import UserTrackedCase

        with app.app_context():
            # First track the case
            service.track_case(str(sample_user.id), str(sample_case.id))

            # Then untrack
            service.untrack_case(str(sample_user.id), str(sample_case.id))

            # Verify record is gone
            record = UserTrackedCase.query.filter_by(
                user_id=sample_user.id, case_id=sample_case.id
            ).first()
            assert record is None

    def test_untrack_case_not_found_raises_error(self, app, service, sample_user, sample_case):
        """Untracking a non-tracked case should raise NotFoundError."""
        from app.middleware.error_handler import NotFoundError

        with app.app_context():
            with pytest.raises(NotFoundError):
                service.untrack_case(str(sample_user.id), str(sample_case.id))


# ---------------------------------------------------------------------------
# get_tracked_cases Tests
# ---------------------------------------------------------------------------


class TestGetTrackedCases:
    """Tests for CaseCacheService.get_tracked_cases."""

    def test_get_tracked_cases_returns_list(self, app, service, sample_user, sample_case):
        """Should return a list of tracked cases with freshness."""
        with app.app_context():
            service.track_case(str(sample_user.id), str(sample_case.id))

            results = service.get_tracked_cases(str(sample_user.id))

            assert len(results) == 1
            assert results[0]["case_number"] == "OA/123/2024"
            assert "freshness" in results[0]
            assert "tracking" in results[0]

    def test_get_tracked_cases_empty(self, app, service, sample_user):
        """Should return empty list when no cases tracked."""
        with app.app_context():
            results = service.get_tracked_cases(str(sample_user.id))
            assert results == []


# ---------------------------------------------------------------------------
# link_cases Tests
# ---------------------------------------------------------------------------


class TestLinkCases:
    """Tests for CaseCacheService.link_cases."""

    def test_link_cases_success(self, app, service, sample_court):
        """Linking two cases should create a relationship record."""
        from app.extensions import db
        from app.models.case import CaseCache

        with app.app_context():
            case1 = CaseCache(
                court_code="aft_del",
                case_number="OA/100/2024",
                case_title="Case One",
                fetched_at=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
            )
            case2 = CaseCache(
                court_code="aft_del",
                case_number="OA/200/2024",
                case_title="Case Two",
                fetched_at=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
            )
            db.session.add_all([case1, case2])
            db.session.commit()

            result = service.link_cases(
                str(case1.id), str(case2.id), "appeal_of"
            )

            assert result["case_id"] == str(case1.id)
            assert result["related_case_id"] == str(case2.id)
            assert result["relationship_type"] == "appeal_of"
            assert result["detected_by"] == "user"
            assert result["confidence"] == 1.0

    def test_link_cases_invalid_type_raises_error(self, app, service, sample_court):
        """Invalid relationship type should raise ValidationError."""
        from app.extensions import db
        from app.middleware.error_handler import ValidationError
        from app.models.case import CaseCache

        with app.app_context():
            case1 = CaseCache(
                court_code="aft_del",
                case_number="OA/300/2024",
                case_title="Case A",
                fetched_at=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
            )
            case2 = CaseCache(
                court_code="aft_del",
                case_number="OA/400/2024",
                case_title="Case B",
                fetched_at=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
            )
            db.session.add_all([case1, case2])
            db.session.commit()

            with pytest.raises(ValidationError, match="Invalid relationship type"):
                service.link_cases(str(case1.id), str(case2.id), "invalid_type")

    def test_link_cases_duplicate_raises_error(self, app, service, sample_court):
        """Duplicate relationship should raise ValidationError."""
        from app.extensions import db
        from app.middleware.error_handler import ValidationError
        from app.models.case import CaseCache

        with app.app_context():
            case1 = CaseCache(
                court_code="aft_del",
                case_number="OA/500/2024",
                case_title="Case X",
                fetched_at=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
            )
            case2 = CaseCache(
                court_code="aft_del",
                case_number="OA/600/2024",
                case_title="Case Y",
                fetched_at=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
            )
            db.session.add_all([case1, case2])
            db.session.commit()

            # First link succeeds
            service.link_cases(str(case1.id), str(case2.id), "writ_against")

            # Duplicate should fail
            with pytest.raises(ValidationError, match="already exists"):
                service.link_cases(str(case1.id), str(case2.id), "writ_against")


# ---------------------------------------------------------------------------
# get_related_cases Tests
# ---------------------------------------------------------------------------


class TestGetRelatedCases:
    """Tests for CaseCacheService.get_related_cases."""

    def test_get_related_cases_both_directions(self, app, service, sample_court):
        """Should return relationships in both directions."""
        from app.extensions import db
        from app.models.case import CaseCache

        with app.app_context():
            case1 = CaseCache(
                court_code="aft_del",
                case_number="OA/700/2024",
                case_title="Case Alpha",
                fetched_at=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
            )
            case2 = CaseCache(
                court_code="aft_del",
                case_number="OA/800/2024",
                case_title="Case Beta",
                fetched_at=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
            )
            case3 = CaseCache(
                court_code="aft_del",
                case_number="OA/900/2024",
                case_title="Case Gamma",
                fetched_at=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
            )
            db.session.add_all([case1, case2, case3])
            db.session.commit()

            # case1 -> case2 (outgoing from case1)
            service.link_cases(str(case1.id), str(case2.id), "appeal_of")
            # case3 -> case1 (incoming to case1)
            service.link_cases(str(case3.id), str(case1.id), "connected_with")

            # Get related for case1 - should have both directions
            results = service.get_related_cases(str(case1.id))

            assert len(results) == 2
            directions = {r["direction"] for r in results}
            assert "outgoing" in directions
            assert "incoming" in directions
