"""Unit tests for OTP utilities, validators, and AuthService."""

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

import pytest

from app.utils.otp import generate_otp, hash_otp, verify_otp_hash
from app.utils.validators import validate_email, validate_phone


# ---------------------------------------------------------------------------
# OTP Generation Tests
# ---------------------------------------------------------------------------


class TestGenerateOTP:
    """Tests for generate_otp function."""

    def test_returns_string(self):
        otp = generate_otp()
        assert isinstance(otp, str)

    def test_exactly_6_digits(self):
        for _ in range(50):
            otp = generate_otp()
            assert len(otp) == 6
            assert otp.isdigit()

    def test_zero_padded(self):
        """OTP should be zero-padded (e.g., '000123' not '123')."""
        # Run many times to increase chance of getting a low number
        results = [generate_otp() for _ in range(100)]
        # All should be exactly 6 chars
        assert all(len(r) == 6 for r in results)

    def test_randomness(self):
        """Multiple calls should produce different values (with high probability)."""
        otps = {generate_otp() for _ in range(20)}
        # With 6 digits (1M possibilities), 20 calls should give at least 2 unique
        assert len(otps) > 1


# ---------------------------------------------------------------------------
# OTP Hash/Verify Tests
# ---------------------------------------------------------------------------


class TestHashAndVerifyOTP:
    """Tests for hash_otp and verify_otp_hash functions."""

    def test_hash_returns_string(self):
        hashed = hash_otp("123456")
        assert isinstance(hashed, str)

    def test_hash_is_bcrypt_format(self):
        hashed = hash_otp("123456")
        # bcrypt hashes start with $2b$ or $2a$
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    def test_verify_correct_code(self):
        code = "654321"
        hashed = hash_otp(code)
        assert verify_otp_hash(code, hashed) is True

    def test_verify_wrong_code(self):
        hashed = hash_otp("123456")
        assert verify_otp_hash("654321", hashed) is False

    def test_verify_empty_code(self):
        hashed = hash_otp("123456")
        assert verify_otp_hash("", hashed) is False

    def test_verify_invalid_hash(self):
        assert verify_otp_hash("123456", "not-a-valid-hash") is False

    def test_round_trip_with_generated_otp(self):
        """Generate → hash → verify should always succeed."""
        for _ in range(10):
            code = generate_otp()
            hashed = hash_otp(code)
            assert verify_otp_hash(code, hashed) is True


# ---------------------------------------------------------------------------
# Email Validation Tests
# ---------------------------------------------------------------------------


class TestValidateEmail:
    """Tests for validate_email function."""

    @pytest.mark.parametrize("email", [
        "user@example.com",
        "test.user@domain.co.in",
        "name+tag@gmail.com",
        "user123@sub.domain.org",
        "a@b.co",
    ])
    def test_valid_emails(self, email):
        assert validate_email(email) is True

    @pytest.mark.parametrize("email", [
        "",
        "not-an-email",
        "@domain.com",
        "user@",
        "user@.com",
        "user@domain",
        "user domain@test.com",
        None,
        123,
    ])
    def test_invalid_emails(self, email):
        assert validate_email(email) is False

    def test_strips_whitespace(self):
        assert validate_email("  user@example.com  ") is True


# ---------------------------------------------------------------------------
# Phone Validation Tests
# ---------------------------------------------------------------------------


class TestValidatePhone:
    """Tests for validate_phone function."""

    @pytest.mark.parametrize("phone", [
        "9876543210",
        "8765432109",
        "7654321098",
        "6543210987",
    ])
    def test_valid_phones(self, phone):
        assert validate_phone(phone) is True

    @pytest.mark.parametrize("phone", [
        "",
        "1234567890",  # starts with 1
        "5234567890",  # starts with 5
        "0987654321",  # starts with 0
        "987654321",   # 9 digits
        "98765432101", # 11 digits
        "abcdefghij",  # letters
        "+919876543210",  # with country code
        None,
        123,
    ])
    def test_invalid_phones(self, phone):
        assert validate_phone(phone) is False

    def test_strips_whitespace(self):
        assert validate_phone("  9876543210  ") is True


# ---------------------------------------------------------------------------
# AuthService Tests (with app context)
# ---------------------------------------------------------------------------


@pytest.fixture
def app(monkeypatch):
    """Create a test Flask app with in-memory SQLite for unit tests."""
    # Set env var BEFORE create_app reads config
    monkeypatch.setenv("TEST_DATABASE_URL", "sqlite:///:memory:")

    # Register UUID type for SQLite compatibility
    from sqlalchemy.dialects.sqlite.base import SQLiteTypeCompiler

    if not hasattr(SQLiteTypeCompiler, 'visit_UUID'):
        SQLiteTypeCompiler.visit_UUID = lambda self, type_, **kw: "CHAR(36)"
    if not hasattr(SQLiteTypeCompiler, 'visit_ARRAY'):
        SQLiteTypeCompiler.visit_ARRAY = lambda self, type_, **kw: "TEXT"
    if not hasattr(SQLiteTypeCompiler, 'visit_JSONB'):
        SQLiteTypeCompiler.visit_JSONB = lambda self, type_, **kw: "TEXT"
    if not hasattr(SQLiteTypeCompiler, 'visit_JSON'):
        SQLiteTypeCompiler.visit_JSON = lambda self, type_, **kw: "TEXT"

    from app import create_app
    from app.extensions import db

    app = create_app("testing")

    with app.app_context():
        # Strip PostgreSQL-specific server_defaults that SQLite can't handle
        # and add Python-side UUID defaults for primary keys
        import uuid as uuid_mod
        for table in db.metadata.tables.values():
            for column in table.columns:
                if column.server_default is not None:
                    sd_text = str(column.server_default.arg)
                    if "uuid_generate_v4" in sd_text or "::" in sd_text:
                        column.server_default = None
                        # Add Python-side default for UUID PKs
                        if column.primary_key and "UUID" in str(type(column.type).__name__).upper():
                            column.default = db.ColumnDefault(uuid_mod.uuid4)

        db.create_all()

        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()


@pytest.fixture
def auth_service(app):
    """AuthService instance within app context."""
    from app.services.auth_service import AuthService
    with app.app_context():
        yield AuthService()


class TestAuthServiceRegister:
    """Tests for AuthService.register_user."""

    def test_register_creates_user_with_defaults(self, app):
        """Registration should create user with tier='free' and is_verified=False."""
        from app.services.auth_service import AuthService
        from app.models.user import User

        with app.app_context():
            service = AuthService()
            user = service.register_user({
                "name": "Test User",
                "email": "test@example.com",
                "phone": "9876543210",
                "user_type": "individual",
            })

            assert user.name == "Test User"
            assert user.email == "test@example.com"
            assert user.phone == "9876543210"
            assert user.tier == "free"
            assert user.is_verified is False
            assert user.user_type == "individual"

    def test_register_advocate_stores_fields(self, app):
        """Advocate registration should store enrollment details."""
        from app.services.auth_service import AuthService

        with app.app_context():
            service = AuthService()
            user = service.register_user({
                "name": "Advocate User",
                "email": "advocate@example.com",
                "phone": "9876543211",
                "user_type": "advocate",
                "enrollment_no": "D/1234/2020",
                "bar_council": "Delhi",
            })

            assert user.user_type == "advocate"
            assert user.enrollment_no == "D/1234/2020"
            assert user.bar_council == "Delhi"
            assert user.tier == "free"

    def test_register_duplicate_email_raises_error(self, app):
        """Duplicate email should raise ValidationError."""
        from app.services.auth_service import AuthService
        from app.middleware.error_handler import ValidationError

        with app.app_context():
            service = AuthService()
            service.register_user({
                "name": "User One",
                "email": "dup@example.com",
                "phone": "9876543210",
                "user_type": "individual",
            })

            with pytest.raises(ValidationError, match="email already exists"):
                service.register_user({
                    "name": "User Two",
                    "email": "dup@example.com",
                    "phone": "9876543211",
                    "user_type": "individual",
                })

    def test_register_duplicate_phone_raises_error(self, app):
        """Duplicate phone should raise ValidationError."""
        from app.services.auth_service import AuthService
        from app.middleware.error_handler import ValidationError

        with app.app_context():
            service = AuthService()
            service.register_user({
                "name": "User One",
                "email": "user1@example.com",
                "phone": "9876543210",
                "user_type": "individual",
            })

            with pytest.raises(ValidationError, match="phone number already exists"):
                service.register_user({
                    "name": "User Two",
                    "email": "user2@example.com",
                    "phone": "9876543210",
                    "user_type": "individual",
                })

    def test_register_invalid_email_raises_error(self, app):
        """Invalid email format should raise ValidationError."""
        from app.services.auth_service import AuthService
        from app.middleware.error_handler import ValidationError

        with app.app_context():
            service = AuthService()
            with pytest.raises(ValidationError, match="Invalid email"):
                service.register_user({
                    "name": "User",
                    "email": "not-an-email",
                    "user_type": "individual",
                })

    def test_register_invalid_phone_raises_error(self, app):
        """Invalid phone format should raise ValidationError."""
        from app.services.auth_service import AuthService
        from app.middleware.error_handler import ValidationError

        with app.app_context():
            service = AuthService()
            with pytest.raises(ValidationError, match="Invalid phone"):
                service.register_user({
                    "name": "User",
                    "phone": "1234567890",
                    "user_type": "individual",
                })

    def test_register_no_email_or_phone_raises_error(self, app):
        """Missing both email and phone should raise ValidationError."""
        from app.services.auth_service import AuthService
        from app.middleware.error_handler import ValidationError

        with app.app_context():
            service = AuthService()
            with pytest.raises(ValidationError, match="Either email or phone"):
                service.register_user({
                    "name": "User",
                    "user_type": "individual",
                })


class TestAuthServiceOTP:
    """Tests for AuthService OTP request and verify."""

    def test_request_otp_email(self, app):
        """request_otp with email should return otp_id and channel='email'."""
        from app.services.auth_service import AuthService

        with app.app_context():
            service = AuthService()
            result = service.request_otp("test@example.com", purpose="login")

            assert "otp_id" in result
            assert result["channel"] == "email"
            assert "expires_at" in result

    def test_request_otp_phone(self, app):
        """request_otp with phone should return otp_id and channel='sms'."""
        from app.services.auth_service import AuthService

        with app.app_context():
            service = AuthService()
            result = service.request_otp("9876543210", purpose="login")

            assert "otp_id" in result
            assert result["channel"] == "sms"
            assert "expires_at" in result

    def test_request_otp_invalid_identifier(self, app):
        """request_otp with invalid identifier should raise ValidationError."""
        from app.services.auth_service import AuthService
        from app.middleware.error_handler import ValidationError

        with app.app_context():
            service = AuthService()
            with pytest.raises(ValidationError, match="Invalid identifier"):
                service.request_otp("invalid")

    def test_verify_otp_success(self, app):
        """Successful OTP verification should return token and user."""
        from app.services.auth_service import AuthService
        from app.utils.otp import hash_otp
        from app.models.otp import OTPToken
        from app.models.user import User
        from app.extensions import db

        with app.app_context():
            service = AuthService()

            # Create a user first
            user = User(
                name="Test User",
                email="verify@example.com",
                phone="9876543210",
                user_type="individual",
                tier="free",
                is_verified=False,
            )
            db.session.add(user)
            db.session.commit()

            # Create an OTP token
            otp_code = "123456"
            otp_token = OTPToken(
                identifier="verify@example.com",
                otp_hash=hash_otp(otp_code),
                purpose="login",
                attempts=0,
                max_attempts=3,
                expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
            )
            db.session.add(otp_token)
            db.session.commit()

            # Verify
            result = service.verify_otp("verify@example.com", otp_code)

            assert "token" in result
            assert result["user"]["email"] == "verify@example.com"
            assert "expires_at" in result

    def test_verify_otp_wrong_code(self, app):
        """Wrong OTP code should raise AuthenticationError."""
        from app.services.auth_service import AuthService
        from app.utils.otp import hash_otp
        from app.models.otp import OTPToken
        from app.models.user import User
        from app.extensions import db
        from app.middleware.error_handler import AuthenticationError

        with app.app_context():
            service = AuthService()

            # Create user
            user = User(
                name="Test User",
                email="wrong@example.com",
                user_type="individual",
                tier="free",
            )
            db.session.add(user)
            db.session.commit()

            # Create OTP
            otp_token = OTPToken(
                identifier="wrong@example.com",
                otp_hash=hash_otp("123456"),
                purpose="login",
                attempts=0,
                max_attempts=3,
                expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
            )
            db.session.add(otp_token)
            db.session.commit()

            with pytest.raises(AuthenticationError, match="Invalid OTP"):
                service.verify_otp("wrong@example.com", "999999")

    def test_verify_otp_expired(self, app):
        """Expired OTP should raise AuthenticationError."""
        from app.services.auth_service import AuthService
        from app.utils.otp import hash_otp
        from app.models.otp import OTPToken
        from app.extensions import db
        from app.middleware.error_handler import AuthenticationError

        with app.app_context():
            service = AuthService()

            # Create expired OTP using naive UTC datetime (matches DB storage)
            expired_time = datetime.utcnow() - timedelta(hours=2)
            otp_token = OTPToken(
                identifier="expired@example.com",
                otp_hash=hash_otp("123456"),
                purpose="login",
                attempts=0,
                max_attempts=3,
                expires_at=expired_time,
            )
            db.session.add(otp_token)
            db.session.flush()
            otp_token.created_at = expired_time - timedelta(hours=1)
            db.session.commit()

            with pytest.raises(AuthenticationError, match="expired"):
                service.verify_otp("expired@example.com", "123456")

    def test_verify_otp_max_attempts(self, app):
        """OTP with max attempts reached should raise AuthenticationError."""
        from app.services.auth_service import AuthService
        from app.utils.otp import hash_otp
        from app.models.otp import OTPToken
        from app.extensions import db
        from app.middleware.error_handler import AuthenticationError

        with app.app_context():
            service = AuthService()

            # Create OTP with max attempts already reached
            otp_token = OTPToken(
                identifier="maxattempts@example.com",
                otp_hash=hash_otp("123456"),
                purpose="login",
                attempts=3,
                max_attempts=3,
                expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
            )
            db.session.add(otp_token)
            db.session.commit()

            with pytest.raises(AuthenticationError, match="Maximum verification attempts"):
                service.verify_otp("maxattempts@example.com", "123456")


class TestAuthServiceLogout:
    """Tests for AuthService.logout."""

    def test_logout_sets_revoked_at(self, app):
        """Logout should set revoked_at on the session."""
        from app.services.auth_service import AuthService
        from app.models.user import User, UserSession
        from app.extensions import db

        with app.app_context():
            service = AuthService()

            # Create user and session
            user = User(
                name="Logout User",
                email="logout@example.com",
                user_type="individual",
                tier="free",
            )
            db.session.add(user)
            db.session.commit()

            session = UserSession(
                user_id=user.id,
                token_hash="abc123hash",
                expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            )
            db.session.add(session)
            db.session.commit()

            session_id = str(session.id)

            # Logout
            service.logout(session_id)

            # Verify
            updated_session = UserSession.query.get(session.id)
            assert updated_session.revoked_at is not None

    def test_logout_nonexistent_session_raises_error(self, app):
        """Logout with invalid session_id should raise NotFoundError."""
        from app.services.auth_service import AuthService
        from app.middleware.error_handler import NotFoundError

        with app.app_context():
            service = AuthService()
            fake_id = str(uuid.uuid4())

            with pytest.raises(NotFoundError, match="Session not found"):
                service.logout(fake_id)
