"""OTP token model mapping to the existing 'otp_tokens' table."""

from sqlalchemy.dialects.postgresql import UUID

from ..extensions import db


class OTPToken(db.Model):
    """Short-lived OTP tokens for passwordless authentication."""

    __tablename__ = "otp_tokens"
    __table_args__ = {"extend_existing": True}

    # Valid purposes
    PURPOSES = ("login", "register", "reset")

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    identifier = db.Column(db.String(255), nullable=False)
    otp_hash = db.Column(db.String(255), nullable=False)
    purpose = db.Column(db.String(20), default="login")
    attempts = db.Column(db.Integer, default=0)
    max_attempts = db.Column(db.Integer, default=3)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def is_expired(self):
        """Check if OTP has expired."""
        from datetime import datetime, timezone

        if not self.expires_at:
            return True
        # Compare as naive datetimes in UTC to avoid timezone conversion issues
        now_utc = datetime.utcnow()
        expires = self.expires_at.replace(tzinfo=None) if self.expires_at.tzinfo else self.expires_at
        return now_utc > expires

    def is_used(self):
        """Check if OTP has already been used."""
        return self.used_at is not None

    def is_max_attempts_reached(self):
        """Check if maximum verification attempts have been reached."""
        return self.attempts >= self.max_attempts

    def is_valid(self):
        """Check if OTP is still valid (not expired, not used, attempts remaining)."""
        return not self.is_expired() and not self.is_used() and not self.is_max_attempts_reached()

    def to_dict(self):
        """Serialize OTP token to a dictionary (excludes hash for security)."""
        return {
            "id": str(self.id),
            "identifier": self.identifier,
            "purpose": self.purpose,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_valid": self.is_valid(),
        }

    def __repr__(self):
        status = "valid" if self.is_valid() else "invalid"
        return f"<OTPToken {self.identifier} ({status})>"
