"""User and UserSession models mapping to existing tables."""

from sqlalchemy.dialects.postgresql import UUID

from ..extensions import db


class User(db.Model):
    """Registered user (individual or advocate)."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    # Valid user types and tiers
    USER_TYPES = ("individual", "advocate")
    TIERS = ("free", "individual", "advocate_normal", "advocate_premium")

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(255))
    user_type = db.Column(db.String(20), nullable=False, default="individual")
    tier = db.Column(db.String(30), nullable=False, default="free")

    # Advocate-specific fields
    enrollment_no = db.Column(db.String(50))
    enrollment_date = db.Column(db.Date)
    bar_council = db.Column(db.String(100))

    # Profile
    address = db.Column(db.Text)
    profile_image_url = db.Column(db.String(500))

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    sessions = db.relationship("UserSession", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")
    subscriptions = db.relationship("Subscription", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")
    tracked_cases = db.relationship("UserTrackedCase", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")

    def to_dict(self, include_private=False):
        """Serialize user to a dictionary for API responses.

        Args:
            include_private: If True, include sensitive fields like email/phone.
        """
        data = {
            "id": str(self.id),
            "name": self.name,
            "user_type": self.user_type,
            "tier": self.tier,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_private:
            data.update({
                "email": self.email,
                "phone": self.phone,
                "enrollment_no": self.enrollment_no,
                "bar_council": self.bar_council,
                "is_active": self.is_active,
            })
        return data

    def __repr__(self):
        return f"<User {self.id}: {self.name} ({self.tier})>"


class UserSession(db.Model):
    """JWT session tracking for users."""

    __tablename__ = "user_sessions"
    __table_args__ = {"extend_existing": True}

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_hash = db.Column(db.String(255), nullable=False)
    device_info = db.Column(db.String(500))
    ip_address = db.Column(db.String(45))
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    user = db.relationship("User", back_populates="sessions")

    def is_active(self):
        """Check if session is still valid (not revoked and not expired)."""
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        if self.revoked_at is not None:
            return False
        if self.expires_at and self.expires_at.replace(tzinfo=timezone.utc) < now:
            return False
        return True

    def to_dict(self):
        """Serialize session to a dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "device_info": self.device_info,
            "ip_address": self.ip_address,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "revoked_at": self.revoked_at.isoformat() if self.revoked_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        status = "revoked" if self.revoked_at else "active"
        return f"<UserSession {self.id} ({status})>"
