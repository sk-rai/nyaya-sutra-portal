"""Authentication service for the Nyaya Sutra Backend API.

Handles OTP generation/verification, JWT issuance, user registration,
and session management.
"""

import hashlib
import logging
from datetime import datetime, timedelta, timezone

from flask_jwt_extended import create_access_token

from ..extensions import db
from ..middleware.error_handler import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
)
from ..models.otp import OTPToken
from ..models.user import User, UserSession
from ..utils.otp import generate_otp, hash_otp, verify_otp_hash
from ..utils.validators import validate_email, validate_phone

logger = logging.getLogger(__name__)


def dispatch_otp(identifier: str, otp_code: str) -> None:
    """Dispatch OTP to the user via the appropriate channel.

    This is a stub/placeholder that logs the OTP to console.
    Will be replaced with Twilio SMS and email service integration later.

    Args:
        identifier: Email address or phone number.
        otp_code: The plaintext OTP code to send.
    """
    if validate_email(identifier):
        logger.info(f"[OTP DISPATCH] Sending OTP {otp_code} to email: {identifier}")
        print(f"[OTP DISPATCH] Email OTP for {identifier}: {otp_code}")
    elif validate_phone(identifier):
        logger.info(f"[OTP DISPATCH] Sending OTP {otp_code} to phone: {identifier}")
        print(f"[OTP DISPATCH] SMS OTP for {identifier}: {otp_code}")
    else:
        logger.warning(f"[OTP DISPATCH] Unknown identifier type: {identifier}")
        print(f"[OTP DISPATCH] OTP for {identifier}: {otp_code}")


class AuthService:
    """Service handling authentication operations."""

    def request_otp(self, identifier: str, purpose: str = "login") -> dict:
        """Generate and dispatch OTP for the given identifier.

        Args:
            identifier: Email address or phone number.
            purpose: Purpose of OTP (login, register, reset).

        Returns:
            Dict with otp_id, expires_at, and channel.

        Raises:
            ValidationError: If identifier is not a valid email or phone.
        """
        # Validate identifier
        is_email = validate_email(identifier)
        is_phone = validate_phone(identifier)

        if not is_email and not is_phone:
            raise ValidationError("Invalid identifier. Must be a valid email or 10-digit Indian mobile number.")

        # Generate OTP
        otp_code = generate_otp()
        otp_hashed = hash_otp(otp_code)

        # Store in database with 10-minute expiry
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

        otp_token = OTPToken(
            identifier=identifier.strip(),
            otp_hash=otp_hashed,
            purpose=purpose,
            attempts=0,
            max_attempts=3,
            expires_at=expires_at,
        )

        db.session.add(otp_token)
        db.session.commit()

        # Dispatch OTP (stub - logs to console)
        dispatch_otp(identifier.strip(), otp_code)

        channel = "email" if is_email else "sms"

        return {
            "otp_id": str(otp_token.id),
            "expires_at": expires_at.isoformat(),
            "channel": channel,
        }

    def verify_otp(self, identifier: str, otp_code: str) -> dict:
        """Verify OTP and issue JWT token.

        Args:
            identifier: Email address or phone number.
            otp_code: The OTP code to verify.

        Returns:
            Dict with token, user data, and expires_at.

        Raises:
            AuthenticationError: If OTP is invalid, expired, or max attempts reached.
            NotFoundError: If user does not exist for the identifier.
        """
        identifier = identifier.strip()

        # Find the latest valid OTP for this identifier
        otp_token = (
            OTPToken.query.filter_by(identifier=identifier)
            .filter(OTPToken.used_at.is_(None))
            .order_by(OTPToken.created_at.desc())
            .first()
        )

        if not otp_token:
            raise AuthenticationError("No valid OTP found for this identifier.")

        # Check if expired
        if otp_token.is_expired():
            raise AuthenticationError("OTP has expired. Please request a new one.")

        # Check max attempts
        if otp_token.is_max_attempts_reached():
            raise AuthenticationError(
                "Maximum verification attempts exceeded. Please request a new OTP."
            )

        # Increment attempts
        otp_token.attempts += 1

        # Verify the OTP hash
        if not verify_otp_hash(otp_code, otp_token.otp_hash):
            db.session.commit()
            raise AuthenticationError("Invalid OTP code.")

        # Mark OTP as used
        otp_token.used_at = datetime.now(timezone.utc)
        db.session.commit()

        # Find user by identifier
        user = User.query.filter(
            (User.email == identifier) | (User.phone == identifier)
        ).first()

        if not user:
            raise NotFoundError("User not found. Please register first.")

        # Mark user as verified
        user.is_verified = True
        user.last_login = datetime.now(timezone.utc)

        # Issue JWT with user_id and tier claims
        additional_claims = {
            "user_id": str(user.id),
            "tier": user.tier,
        }
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims,
        )

        # Create session record
        token_hash = hashlib.sha256(access_token.encode("utf-8")).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        session = UserSession(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        db.session.add(session)
        db.session.commit()

        return {
            "token": access_token,
            "user": user.to_dict(include_private=True),
            "expires_at": expires_at.isoformat(),
        }

    def register_user(self, data: dict) -> User:
        """Register a new user.

        Args:
            data: Dict with name, email, phone, user_type, and optional
                  advocate fields (enrollment_no, enrollment_date, bar_council).

        Returns:
            The created User instance.

        Raises:
            ValidationError: If inputs are invalid or duplicates exist.
        """
        name = data.get("name", "").strip()
        email = data.get("email", "").strip() if data.get("email") else None
        phone = data.get("phone", "").strip() if data.get("phone") else None
        user_type = data.get("user_type", "individual")

        # Validate required fields
        if not name:
            raise ValidationError("Name is required.")

        if not email and not phone:
            raise ValidationError("Either email or phone is required.")

        # Validate email format
        if email and not validate_email(email):
            raise ValidationError("Invalid email format.")

        # Validate phone format
        if phone and not validate_phone(phone):
            raise ValidationError("Invalid phone number. Must be a 10-digit Indian mobile number starting with 6-9.")

        # Validate user_type
        if user_type not in User.USER_TYPES:
            raise ValidationError(f"Invalid user_type. Must be one of: {', '.join(User.USER_TYPES)}")

        # Check for duplicate email
        if email:
            existing = User.query.filter_by(email=email).first()
            if existing:
                raise ValidationError("A user with this email already exists.")

        # Check for duplicate phone
        if phone:
            existing = User.query.filter_by(phone=phone).first()
            if existing:
                raise ValidationError("A user with this phone number already exists.")

        # Create user with defaults
        user = User(
            name=name,
            email=email,
            phone=phone,
            user_type=user_type,
            tier="free",
            is_verified=False,
        )

        # Store advocate-specific fields
        if user_type == "advocate":
            user.enrollment_no = data.get("enrollment_no")
            user.enrollment_date = data.get("enrollment_date")
            user.bar_council = data.get("bar_council")

        db.session.add(user)
        db.session.commit()

        return user

    def logout(self, session_id: str) -> None:
        """Revoke a user session.

        Args:
            session_id: The UUID of the session to revoke (as string).

        Raises:
            NotFoundError: If the session does not exist.
        """
        import uuid as uuid_mod
        try:
            sid = uuid_mod.UUID(session_id) if isinstance(session_id, str) else session_id
        except (ValueError, AttributeError):
            raise NotFoundError("Session not found.")

        session = db.session.get(UserSession, sid)

        if not session:
            raise NotFoundError("Session not found.")

        session.revoked_at = datetime.now(timezone.utc)
        db.session.commit()
