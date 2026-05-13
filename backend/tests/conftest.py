"""Shared pytest fixtures for the Nyaya Sutra Backend test suite.

Provides:
- test_app: Flask app configured for testing (uses nyaya_sutra_test DB)
- client: Flask test client
- db_session: Database session with automatic rollback
- auth_headers: Helper to generate JWT auth headers
- sample_user: Pre-created test user
- sample_court: Pre-created test court
"""

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def test_app():
    """Create a Flask app for the full test session.

    Uses the 'testing' config which points to nyaya_sutra_test database.
    """
    app = create_app("testing")
    yield app


@pytest.fixture(scope="function")
def app(test_app):
    """Per-test app context with transaction rollback.

    Each test runs in a nested transaction that is rolled back after,
    keeping the test database clean.
    """
    with test_app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()

        # Bind session to this connection
        options = dict(bind=connection, binds={})
        session = _db.create_scoped_session(options=options)
        _db.session = session

        yield test_app

        # Rollback after each test
        transaction.rollback()
        connection.close()
        session.remove()


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """Database session for direct DB operations in tests."""
    return _db.session


@pytest.fixture
def sample_court(app, db_session):
    """Create a sample court for testing."""
    from app.models.court import Court

    court = Court.query.get("aft_del")
    if court:
        return court

    # If not in DB, the schema should have seeded it
    # Return the first available court
    court = Court.query.first()
    return court


@pytest.fixture
def sample_user(app, db_session):
    """Create a sample test user."""
    from app.models.user import User

    user = User(
        name="Test User",
        email=f"test_{uuid.uuid4().hex[:8]}@example.com",
        phone=f"98765{uuid.uuid4().int % 100000:05d}",
        user_type="individual",
        tier="free",
        is_verified=True,
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def sample_advocate(app, db_session):
    """Create a sample advocate user with premium tier."""
    from app.models.user import User

    user = User(
        name="Test Advocate",
        email=f"advocate_{uuid.uuid4().hex[:8]}@example.com",
        phone=f"98764{uuid.uuid4().int % 100000:05d}",
        user_type="advocate",
        tier="advocate_premium",
        is_verified=True,
        enrollment_no="DEL/1234/2020",
        bar_council="Delhi",
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def auth_headers(app, sample_user):
    """Generate JWT auth headers for the sample user."""
    from flask_jwt_extended import create_access_token

    with app.app_context():
        token = create_access_token(
            identity=str(sample_user.id),
            additional_claims={
                "user_id": str(sample_user.id),
                "tier": sample_user.tier,
            },
        )
        return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def premium_auth_headers(app, sample_advocate):
    """Generate JWT auth headers for a premium advocate user."""
    from flask_jwt_extended import create_access_token

    with app.app_context():
        token = create_access_token(
            identity=str(sample_advocate.id),
            additional_claims={
                "user_id": str(sample_advocate.id),
                "tier": sample_advocate.tier,
            },
        )
        return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_scraper():
    """Mock the scraper to avoid real HTTP calls during tests."""
    from app.scrapers.base import ScrapeResult

    mock_result = ScrapeResult(
        structured={
            "case_number": "OA 123/2024",
            "case_title": "John Doe vs Union of India",
            "petitioner": "John Doe",
            "respondent": "Union of India",
            "advocate_petitioner": "Adv. Smith",
            "bench": "Principal Bench",
            "item_number": "1",
            "next_hearing_date": "2024-04-15",
        },
        raw_data="1 | OA 123/2024 | John Doe vs Union of India | Adv. Smith",
        confidence=0.85,
        parse_errors=[],
        source_url="https://aftdelhi.nic.in/cause-list",
        source_page=1,
    )

    with patch(
        "app.scrapers.registry.ScraperFactory.get_scraper"
    ) as mock_factory:
        mock_scraper_instance = type("MockScraper", (), {
            "scrape": lambda self, court_code, case_number: mock_result,
        })()
        mock_factory.return_value = mock_scraper_instance
        yield mock_factory


@pytest.fixture
def mock_razorpay():
    """Mock Razorpay client for payment tests."""
    with patch("app.services.payment_service.razorpay") as mock_rp:
        mock_client = type("MockClient", (), {
            "order": type("MockOrder", (), {
                "create": lambda self, data: {
                    "id": "order_test123",
                    "amount": data.get("amount", 5000),
                    "currency": "INR",
                    "status": "created",
                },
            })(),
            "utility": type("MockUtility", (), {
                "verify_payment_signature": lambda self, data: True,
            })(),
        })()
        mock_rp.Client.return_value = mock_client
        yield mock_rp
