"""Case-related models mapping to existing tables.

Includes CaseCache, CaseHearing, and CaseRelationship.
"""

from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID

from ..extensions import db


class CaseCache(db.Model):
    """On-demand case cache. Fetched from court PDFs when users search.

    Anti-fragile design: stores both structured fields AND raw scraped data
    as JSONB. If PDF format changes, raw data allows re-parsing later.
    """

    __tablename__ = "case_cache"
    __table_args__ = (
        db.UniqueConstraint("court_code", "case_number", name="uq_case_cache_court_number"),
        {"extend_existing": True},
    )

    # Case status constants
    STATUSES = ("pending", "disposed", "reserved", "part_heard")

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    court_code = db.Column(db.String(30), db.ForeignKey("courts.code"), nullable=False)
    case_number = db.Column(db.String(150), nullable=False)

    # Structured fields (best-effort parsed from PDF)
    case_title = db.Column(db.String(500))
    petitioner = db.Column(db.String(500))
    respondent = db.Column(db.String(500))
    advocate_petitioner = db.Column(db.String(500))
    advocate_respondent = db.Column(db.String(500))
    bench = db.Column(db.String(255))
    item_number = db.Column(db.String(20))
    case_type = db.Column(db.String(50))
    case_status = db.Column(db.String(50))

    # Hearing dates
    next_hearing_date = db.Column(db.Date)
    last_hearing_date = db.Column(db.Date)

    # Anti-fragility: raw data preserved as-is
    raw_scraped_data = db.Column(JSON)
    parse_confidence = db.Column(db.Float, default=1.0)
    parse_errors = db.Column(ARRAY(db.Text))
    extra_fields = db.Column(JSON, server_default=db.text("'{}'::jsonb"))

    # Source tracking
    source_url = db.Column(db.String(500))
    source_page_number = db.Column(db.Integer)

    # Cache management
    is_tracked = db.Column(db.Boolean, default=False)
    tracked_by_count = db.Column(db.Integer, default=0)
    fetched_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    last_accessed_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    last_refreshed_at = db.Column(db.DateTime)
    refresh_count = db.Column(db.Integer, default=0)

    # Scraper version
    scraper_version = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    court = db.relationship("Court", back_populates="cases")
    hearings = db.relationship("CaseHearing", back_populates="case", lazy="dynamic", cascade="all, delete-orphan")
    tracked_by = db.relationship("UserTrackedCase", back_populates="case", lazy="dynamic", cascade="all, delete-orphan")
    relationships_as_source = db.relationship(
        "CaseRelationship",
        foreign_keys="CaseRelationship.case_id",
        back_populates="case",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    relationships_as_related = db.relationship(
        "CaseRelationship",
        foreign_keys="CaseRelationship.related_case_id",
        back_populates="related_case",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def get_freshness(self):
        """Calculate freshness based on fetched_at timestamp.

        Returns:
            str: 'fresh' (<6h), 'recent' (<24h), 'stale' (<48h), 'very_stale' (>48h)
        """
        from datetime import datetime, timezone, timedelta

        if not self.fetched_at:
            return "very_stale"

        now = datetime.now(timezone.utc)
        fetched = self.fetched_at.replace(tzinfo=timezone.utc) if self.fetched_at.tzinfo is None else self.fetched_at
        age = now - fetched

        if age < timedelta(hours=6):
            return "fresh"
        elif age < timedelta(hours=24):
            return "recent"
        elif age < timedelta(hours=48):
            return "stale"
        else:
            return "very_stale"

    def to_dict(self, include_raw=False):
        """Serialize case to a dictionary for API responses.

        Args:
            include_raw: If True, include raw_scraped_data and extra_fields.
        """
        data = {
            "id": str(self.id),
            "court_code": self.court_code,
            "case_number": self.case_number,
            "case_title": self.case_title,
            "petitioner": self.petitioner,
            "respondent": self.respondent,
            "advocate_petitioner": self.advocate_petitioner,
            "advocate_respondent": self.advocate_respondent,
            "bench": self.bench,
            "item_number": self.item_number,
            "case_type": self.case_type,
            "case_status": self.case_status,
            "next_hearing_date": self.next_hearing_date.isoformat() if self.next_hearing_date else None,
            "last_hearing_date": self.last_hearing_date.isoformat() if self.last_hearing_date else None,
            "parse_confidence": self.parse_confidence,
            "is_tracked": self.is_tracked,
            "tracked_by_count": self.tracked_by_count,
            "freshness": self.get_freshness(),
            "fetched_at": self.fetched_at.isoformat() if self.fetched_at else None,
            "last_refreshed_at": self.last_refreshed_at.isoformat() if self.last_refreshed_at else None,
        }
        if include_raw:
            data["raw_scraped_data"] = self.raw_scraped_data
            data["extra_fields"] = self.extra_fields
            data["parse_errors"] = self.parse_errors
        return data

    def __repr__(self):
        return f"<CaseCache {self.court_code}/{self.case_number}>"


class CaseHearing(db.Model):
    """Historical hearing records for tracked cases."""

    __tablename__ = "case_hearings"
    __table_args__ = (
        db.UniqueConstraint("case_id", "hearing_date", name="uq_case_hearings_case_date"),
        {"extend_existing": True},
    )

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    case_id = db.Column(UUID(as_uuid=True), db.ForeignKey("case_cache.id", ondelete="CASCADE"), nullable=False)
    hearing_date = db.Column(db.Date, nullable=False)
    bench = db.Column(db.String(255))
    item_number = db.Column(db.String(20))
    order_summary = db.Column(db.Text)
    order_pdf_url = db.Column(db.String(500))
    raw_data = db.Column(JSON)
    fetched_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    case = db.relationship("CaseCache", back_populates="hearings")

    def to_dict(self):
        """Serialize hearing to a dictionary."""
        return {
            "id": str(self.id),
            "case_id": str(self.case_id),
            "hearing_date": self.hearing_date.isoformat() if self.hearing_date else None,
            "bench": self.bench,
            "item_number": self.item_number,
            "order_summary": self.order_summary,
            "order_pdf_url": self.order_pdf_url,
            "fetched_at": self.fetched_at.isoformat() if self.fetched_at else None,
        }

    def __repr__(self):
        return f"<CaseHearing {self.case_id} on {self.hearing_date}>"


class CaseRelationship(db.Model):
    """Cross-court case linkages (e.g., appeal, writ, SLP)."""

    __tablename__ = "case_relationships"
    __table_args__ = (
        db.UniqueConstraint("case_id", "related_case_id", "relationship_type", name="uq_case_relationships"),
        {"extend_existing": True},
    )

    # Valid relationship types
    RELATIONSHIP_TYPES = (
        "appeal_of",
        "writ_against",
        "slp_against",
        "transfer_from",
        "connected_with",
        "contempt_of",
    )

    # Detection sources
    DETECTED_BY_OPTIONS = ("user", "system")

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    case_id = db.Column(UUID(as_uuid=True), db.ForeignKey("case_cache.id", ondelete="CASCADE"), nullable=False)
    related_case_id = db.Column(UUID(as_uuid=True), db.ForeignKey("case_cache.id", ondelete="CASCADE"), nullable=False)
    relationship_type = db.Column(db.String(30), nullable=False)
    detected_by = db.Column(db.String(20), nullable=False, default="user")
    confidence = db.Column(db.Float, default=1.0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    case = db.relationship("CaseCache", foreign_keys=[case_id], back_populates="relationships_as_source")
    related_case = db.relationship("CaseCache", foreign_keys=[related_case_id], back_populates="relationships_as_related")

    def to_dict(self):
        """Serialize relationship to a dictionary."""
        return {
            "id": str(self.id),
            "case_id": str(self.case_id),
            "related_case_id": str(self.related_case_id),
            "relationship_type": self.relationship_type,
            "detected_by": self.detected_by,
            "confidence": self.confidence,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<CaseRelationship {self.case_id} -{self.relationship_type}-> {self.related_case_id}>"
