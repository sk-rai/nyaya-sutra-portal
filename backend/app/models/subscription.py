"""Subscription model mapping to the existing 'subscriptions' table."""

from sqlalchemy.dialects.postgresql import UUID

from ..extensions import db


class Subscription(db.Model):
    """Payment and subscription tracking for tier upgrades."""

    __tablename__ = "subscriptions"
    __table_args__ = {"extend_existing": True}

    # Valid statuses
    STATUSES = ("active", "expired", "cancelled", "payment_failed")

    # Valid tiers for paid subscriptions
    PAID_TIERS = ("individual", "advocate_normal", "advocate_premium")

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tier = db.Column(db.String(30), nullable=False)
    amount_paise = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), default="INR")

    # Payment gateway details
    payment_gateway = db.Column(db.String(20))
    gateway_subscription_id = db.Column(db.String(255))
    gateway_payment_id = db.Column(db.String(255))

    # Dates
    started_at = db.Column(db.DateTime, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    cancelled_at = db.Column(db.DateTime)

    # Status
    status = db.Column(db.String(20), nullable=False, default="active")

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    user = db.relationship("User", back_populates="subscriptions")

    def is_expired(self):
        """Check if subscription has expired."""
        from datetime import datetime, timezone

        if not self.expires_at:
            return True
        now = datetime.now(timezone.utc)
        expires = self.expires_at.replace(tzinfo=timezone.utc) if self.expires_at.tzinfo is None else self.expires_at
        return expires < now

    def is_active_subscription(self):
        """Check if subscription is currently active and not expired."""
        return self.status == "active" and not self.is_expired()

    def to_dict(self):
        """Serialize subscription to a dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "tier": self.tier,
            "amount_paise": self.amount_paise,
            "currency": self.currency,
            "payment_gateway": self.payment_gateway,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "cancelled_at": self.cancelled_at.isoformat() if self.cancelled_at else None,
        }

    def __repr__(self):
        return f"<Subscription {self.id}: {self.tier} ({self.status})>"
