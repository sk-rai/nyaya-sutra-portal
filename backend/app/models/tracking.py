"""User tracked case model mapping to the existing 'user_tracked_cases' table."""

from sqlalchemy.dialects.postgresql import UUID

from ..extensions import db


class UserTrackedCase(db.Model):
    """Cases that a user is actively tracking with alert preferences."""

    __tablename__ = "user_tracked_cases"
    __table_args__ = (
        db.UniqueConstraint("user_id", "case_id", name="uq_user_tracked_cases"),
        {"extend_existing": True},
    )

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    case_id = db.Column(UUID(as_uuid=True), db.ForeignKey("case_cache.id", ondelete="CASCADE"), nullable=False)

    # Alert preferences
    alert_enabled = db.Column(db.Boolean, default=True)
    alert_sms = db.Column(db.Boolean, default=False)
    alert_whatsapp = db.Column(db.Boolean, default=False)
    alert_email = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

    added_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    user = db.relationship("User", back_populates="tracked_cases")
    case = db.relationship("CaseCache", back_populates="tracked_by")

    def to_dict(self):
        """Serialize tracked case to a dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "case_id": str(self.case_id),
            "alert_enabled": self.alert_enabled,
            "alert_sms": self.alert_sms,
            "alert_whatsapp": self.alert_whatsapp,
            "alert_email": self.alert_email,
            "notes": self.notes,
            "added_at": self.added_at.isoformat() if self.added_at else None,
        }

    def __repr__(self):
        return f"<UserTrackedCase user={self.user_id} case={self.case_id}>"
