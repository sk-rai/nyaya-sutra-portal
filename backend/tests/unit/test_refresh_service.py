"""Unit tests for RefreshService."""

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

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


# ---------------------------------------------------------------------------
# refresh_tracked_cases Tests
# ---------------------------------------------------------------------------


class TestRefreshTrackedCases:
    """Tests for RefreshService.refresh_tracked_cases."""

    def test_refresh_no_cases_needing_refresh(self, app):
        """When no cases need refresh, should return all zeros."""
        from app.services.refresh_service import RefreshService

        with app.app_context():
            service = RefreshService()

            # Mock get_cases_needing_refresh to return empty list
            with patch.object(service, "get_cases_needing_refresh", return_value=[]):
                result = service.refresh_tracked_cases()

            assert result == {"refreshed": 0, "failed": 0, "skipped": 0}

    def test_refresh_skips_all_cases_without_scraper(self, app):
        """Without scrapers, all cases should be skipped."""
        from app.services.refresh_service import RefreshService

        with app.app_context():
            service = RefreshService()

            mock_cases = [
                {"case_id": "id-1", "court_code": "aft_del", "case_number": "OA/1/2024", "source_url": None, "max_tier": "free"},
                {"case_id": "id-2", "court_code": "cat_del", "case_number": "OA/2/2024", "source_url": None, "max_tier": "individual"},
                {"case_id": "id-3", "court_code": "hc_del", "case_number": "WP/3/2024", "source_url": None, "max_tier": "advocate_premium"},
            ]

            with patch.object(service, "get_cases_needing_refresh", return_value=mock_cases):
                result = service.refresh_tracked_cases(batch_size=2, delay_sec=0)

            assert result["refreshed"] == 0
            assert result["failed"] == 0
            assert result["skipped"] == 3

    def test_refresh_respects_batch_size(self, app):
        """Should process cases in batches."""
        from app.services.refresh_service import RefreshService

        with app.app_context():
            service = RefreshService()

            # Create 5 mock cases
            mock_cases = [
                {"case_id": f"id-{i}", "court_code": "aft_del", "case_number": f"OA/{i}/2024", "source_url": None, "max_tier": "free"}
                for i in range(5)
            ]

            with patch.object(service, "get_cases_needing_refresh", return_value=mock_cases):
                result = service.refresh_tracked_cases(batch_size=2, delay_sec=0)

            assert result["skipped"] == 5


# ---------------------------------------------------------------------------
# purge_stale_cache Tests
# ---------------------------------------------------------------------------


class TestPurgeStaleCache:
    """Tests for RefreshService.purge_stale_cache."""

    def test_purge_stale_cache_success(self, app):
        """Should call DB function and return counts."""
        from app.services.refresh_service import RefreshService
        from app.extensions import db

        with app.app_context():
            service = RefreshService()

            # Mock the DB function call since SQLite doesn't have it
            mock_result = MagicMock()
            mock_result.fetchone.return_value = (5, 10, 3, 2)

            with patch.object(db.session, "execute", return_value=mock_result):
                with patch.object(db.session, "commit"):
                    result = service.purge_stale_cache()

            assert result["deleted_cases"] == 5
            assert result["deleted_hearings"] == 10
            assert result["deleted_otps"] == 3
            assert result["deleted_sessions"] == 2

    def test_purge_stale_cache_empty_result(self, app):
        """Should handle empty result from DB function."""
        from app.services.refresh_service import RefreshService
        from app.extensions import db

        with app.app_context():
            service = RefreshService()

            mock_result = MagicMock()
            mock_result.fetchone.return_value = None

            with patch.object(db.session, "execute", return_value=mock_result):
                with patch.object(db.session, "commit"):
                    result = service.purge_stale_cache()

            assert result == {
                "deleted_cases": 0,
                "deleted_hearings": 0,
                "deleted_otps": 0,
                "deleted_sessions": 0,
            }

    def test_purge_stale_cache_handles_exception(self, app):
        """Should handle DB errors gracefully."""
        from app.services.refresh_service import RefreshService
        from app.extensions import db

        with app.app_context():
            service = RefreshService()

            with patch.object(db.session, "execute", side_effect=Exception("DB error")):
                with patch.object(db.session, "rollback"):
                    result = service.purge_stale_cache()

            assert result == {
                "deleted_cases": 0,
                "deleted_hearings": 0,
                "deleted_otps": 0,
                "deleted_sessions": 0,
            }


# ---------------------------------------------------------------------------
# get_cases_needing_refresh Tests
# ---------------------------------------------------------------------------


class TestGetCasesNeedingRefresh:
    """Tests for RefreshService.get_cases_needing_refresh."""

    def test_get_cases_needing_refresh_success(self, app):
        """Should call DB function and return list of case dicts."""
        from app.services.refresh_service import RefreshService
        from app.extensions import db

        with app.app_context():
            service = RefreshService()

            case_id = uuid.uuid4()
            mock_result = MagicMock()
            mock_result.fetchall.return_value = [
                (case_id, "aft_del", "OA/1/2024", "http://court.example.com/1", "individual"),
                (uuid.uuid4(), "cat_del", "OA/2/2024", None, "free"),
            ]

            with patch.object(db.session, "execute", return_value=mock_result):
                result = service.get_cases_needing_refresh()

            assert len(result) == 2
            assert result[0]["case_id"] == str(case_id)
            assert result[0]["court_code"] == "aft_del"
            assert result[0]["case_number"] == "OA/1/2024"
            assert result[0]["source_url"] == "http://court.example.com/1"
            assert result[0]["max_tier"] == "individual"

    def test_get_cases_needing_refresh_empty(self, app):
        """Should return empty list when no cases need refresh."""
        from app.services.refresh_service import RefreshService
        from app.extensions import db

        with app.app_context():
            service = RefreshService()

            mock_result = MagicMock()
            mock_result.fetchall.return_value = []

            with patch.object(db.session, "execute", return_value=mock_result):
                result = service.get_cases_needing_refresh()

            assert result == []

    def test_get_cases_needing_refresh_handles_exception(self, app):
        """Should handle DB errors gracefully and return empty list."""
        from app.services.refresh_service import RefreshService
        from app.extensions import db

        with app.app_context():
            service = RefreshService()

            with patch.object(db.session, "execute", side_effect=Exception("DB error")):
                result = service.get_cases_needing_refresh()

            assert result == []
