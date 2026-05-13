"""Unit tests for PaymentService."""

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


@pytest.fixture
def payment_service(app):
    """PaymentService instance within app context."""
    from app.services.payment_service import PaymentService

    with app.app_context():
        yield PaymentService()


# ---------------------------------------------------------------------------
# create_order Tests
# ---------------------------------------------------------------------------


class TestCreateOrder:
    """Tests for PaymentService.create_order."""

    def test_create_order_mock_mode_individual(self, app):
        """Mock mode should return a fake order for individual tier."""
        from app.services.payment_service import PaymentService

        with app.app_context():
            service = PaymentService()
            result = service.create_order("user-123", "individual")

            assert result["order_id"].startswith("order_mock_")
            assert result["amount"] == 5000
            assert result["currency"] == "INR"
            assert result["tier"] == "individual"
            assert result["key_id"] == "rzp_test_mock"

    def test_create_order_mock_mode_advocate_normal(self, app):
        """Mock mode should return correct amount for advocate_normal."""
        from app.services.payment_service import PaymentService

        with app.app_context():
            service = PaymentService()
            result = service.create_order("user-456", "advocate_normal")

            assert result["amount"] == 19900
            assert result["tier"] == "advocate_normal"

    def test_create_order_mock_mode_advocate_premium(self, app):
        """Mock mode should return correct amount for advocate_premium."""
        from app.services.payment_service import PaymentService

        with app.app_context():
            service = PaymentService()
            result = service.create_order("user-789", "advocate_premium")

            assert result["amount"] == 59900
            assert result["tier"] == "advocate_premium"

    def test_create_order_invalid_tier_raises_error(self, app):
        """Invalid tier should raise ValidationError."""
        from app.services.payment_service import PaymentService
        from app.middleware.error_handler import ValidationError

        with app.app_context():
            service = PaymentService()
            with pytest.raises(ValidationError, match="Invalid tier"):
                service.create_order("user-123", "nonexistent_tier")

    def test_create_order_free_tier_raises_error(self, app):
        """Free tier is not a paid tier and should raise ValidationError."""
        from app.services.payment_service import PaymentService
        from app.middleware.error_handler import ValidationError

        with app.app_context():
            service = PaymentService()
            with pytest.raises(ValidationError, match="Invalid tier"):
                service.create_order("user-123", "free")


# ---------------------------------------------------------------------------
# verify_payment Tests
# ---------------------------------------------------------------------------


class TestVerifyPayment:
    """Tests for PaymentService.verify_payment."""

    def test_verify_payment_mock_mode_returns_true(self, app):
        """Mock mode should always return True."""
        from app.services.payment_service import PaymentService

        with app.app_context():
            service = PaymentService()
            result = service.verify_payment({
                "razorpay_order_id": "order_mock_123",
                "razorpay_payment_id": "pay_mock_456",
                "razorpay_signature": "fake_signature",
            })

            assert result is True

    def test_verify_payment_mock_mode_empty_data(self, app):
        """Mock mode should return True even with empty data."""
        from app.services.payment_service import PaymentService

        with app.app_context():
            service = PaymentService()
            result = service.verify_payment({})

            assert result is True


# ---------------------------------------------------------------------------
# handle_webhook Tests
# ---------------------------------------------------------------------------


class TestHandleWebhook:
    """Tests for PaymentService.handle_webhook."""

    def test_handle_webhook_payment_captured_creates_subscription(self, app):
        """payment.captured should create subscription and upgrade tier."""
        from app.services.payment_service import PaymentService
        from app.models.user import User
        from app.models.subscription import Subscription
        from app.extensions import db

        with app.app_context():
            service = PaymentService()

            # Create a user
            user = User(
                name="Webhook User",
                email="webhook@example.com",
                phone="9876543210",
                user_type="individual",
                tier="free",
                is_verified=True,
            )
            db.session.add(user)
            db.session.commit()
            user_id = str(user.id)

            # Simulate webhook payload
            payload = {
                "event": "payment.captured",
                "payload": {
                    "payment": {
                        "entity": {
                            "id": "pay_test_123",
                            "order_id": "order_test_456",
                            "amount": 5000,
                            "notes": {
                                "user_id": user_id,
                                "tier": "individual",
                            },
                        }
                    }
                },
            }

            result = service.handle_webhook(payload, "mock_signature")

            assert result["status"] == "success"
            assert result["user_id"] == user_id
            assert result["tier"] == "individual"

            # Verify user tier was updated
            updated_user = db.session.get(User, user.id)
            assert updated_user.tier == "individual"

            # Verify subscription was created
            sub = Subscription.query.filter_by(user_id=user.id).first()
            assert sub is not None
            assert sub.tier == "individual"
            assert sub.amount_paise == 5000
            assert sub.status == "active"
            assert sub.gateway_payment_id == "pay_test_123"

    def test_handle_webhook_payment_failed_preserves_tier(self, app):
        """payment.failed should not change user tier."""
        from app.services.payment_service import PaymentService
        from app.models.user import User
        from app.extensions import db

        with app.app_context():
            service = PaymentService()

            # Create a user with existing tier
            user = User(
                name="Failed Payment User",
                email="failed@example.com",
                phone="9876543211",
                user_type="individual",
                tier="individual",
                is_verified=True,
            )
            db.session.add(user)
            db.session.commit()
            user_id = str(user.id)

            # Simulate failed payment webhook
            payload = {
                "event": "payment.failed",
                "payload": {
                    "payment": {
                        "entity": {
                            "id": "pay_failed_123",
                            "order_id": "order_failed_456",
                            "error_code": "BAD_REQUEST_ERROR",
                            "error_description": "Payment failed",
                            "notes": {
                                "user_id": user_id,
                                "tier": "advocate_premium",
                            },
                        }
                    }
                },
            }

            result = service.handle_webhook(payload, "mock_signature")

            assert result["status"] == "failed"

            # Verify user tier was NOT changed
            updated_user = db.session.get(User, user.id)
            assert updated_user.tier == "individual"

    def test_handle_webhook_unknown_event_ignored(self, app):
        """Unknown events should be ignored."""
        from app.services.payment_service import PaymentService

        with app.app_context():
            service = PaymentService()

            payload = {"event": "order.paid", "payload": {}}
            result = service.handle_webhook(payload, "mock_signature")

            assert result["status"] == "ignored"


# ---------------------------------------------------------------------------
# check_expiry Tests
# ---------------------------------------------------------------------------


class TestCheckExpiry:
    """Tests for PaymentService.check_expiry."""

    def test_check_expiry_downgrades_expired_subscriptions(self, app):
        """Expired subscriptions should downgrade user to free tier."""
        from app.services.payment_service import PaymentService
        from app.models.user import User
        from app.models.subscription import Subscription
        from app.extensions import db

        with app.app_context():
            service = PaymentService()

            # Create a user with paid tier
            user = User(
                name="Expiry User",
                email="expiry@example.com",
                phone="9876543212",
                user_type="individual",
                tier="advocate_normal",
                is_verified=True,
            )
            db.session.add(user)
            db.session.commit()

            # Create an expired subscription
            sub = Subscription(
                user_id=user.id,
                tier="advocate_normal",
                amount_paise=19900,
                currency="INR",
                payment_gateway="razorpay",
                started_at=datetime.now(timezone.utc) - timedelta(days=31),
                expires_at=datetime.now(timezone.utc) - timedelta(days=1),
                status="active",
            )
            db.session.add(sub)
            db.session.commit()

            # Run expiry check
            affected = service.check_expiry()

            assert str(user.id) in affected

            # Verify user was downgraded
            updated_user = db.session.get(User, user.id)
            assert updated_user.tier == "free"

            # Verify subscription status
            updated_sub = db.session.get(Subscription, sub.id)
            assert updated_sub.status == "expired"

    def test_check_expiry_ignores_active_subscriptions(self, app):
        """Active (non-expired) subscriptions should not be affected."""
        from app.services.payment_service import PaymentService
        from app.models.user import User
        from app.models.subscription import Subscription
        from app.extensions import db

        with app.app_context():
            service = PaymentService()

            # Create a user with paid tier
            user = User(
                name="Active User",
                email="active@example.com",
                phone="9876543213",
                user_type="individual",
                tier="advocate_premium",
                is_verified=True,
            )
            db.session.add(user)
            db.session.commit()

            # Create an active (not expired) subscription
            sub = Subscription(
                user_id=user.id,
                tier="advocate_premium",
                amount_paise=59900,
                currency="INR",
                payment_gateway="razorpay",
                started_at=datetime.now(timezone.utc) - timedelta(days=10),
                expires_at=datetime.now(timezone.utc) + timedelta(days=20),
                status="active",
            )
            db.session.add(sub)
            db.session.commit()

            # Run expiry check
            affected = service.check_expiry()

            assert affected == []

            # Verify user tier unchanged
            updated_user = db.session.get(User, user.id)
            assert updated_user.tier == "advocate_premium"

    def test_check_expiry_no_subscriptions(self, app):
        """No subscriptions should return empty list."""
        from app.services.payment_service import PaymentService

        with app.app_context():
            service = PaymentService()
            affected = service.check_expiry()
            assert affected == []
