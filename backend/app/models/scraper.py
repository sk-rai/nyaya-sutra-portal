"""Scraper-related models mapping to existing tables.

Includes ScraperRegistry, ScrapeLog, and PdfFormatSignature.
"""

from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID

from ..extensions import db


class ScraperRegistry(db.Model):
    """Tracks scraper health per court. Detects PDF format changes via failure patterns."""

    __tablename__ = "scraper_registry"
    __table_args__ = (
        db.UniqueConstraint("court_code", "scraper_version", name="uq_scraper_registry_court_version"),
        {"extend_existing": True},
    )

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    court_code = db.Column(db.String(30), db.ForeignKey("courts.code"), nullable=False)
    scraper_version = db.Column(db.String(20), nullable=False)

    # Health metrics
    last_run_at = db.Column(db.DateTime)
    last_success_at = db.Column(db.DateTime)
    last_failure_at = db.Column(db.DateTime)
    consecutive_failures = db.Column(db.Integer, default=0)
    total_runs = db.Column(db.Integer, default=0)
    total_successes = db.Column(db.Integer, default=0)
    total_failures = db.Column(db.Integer, default=0)
    avg_parse_confidence = db.Column(db.Float)

    # Alert thresholds
    is_healthy = db.Column(db.Boolean, default=True)
    failure_threshold = db.Column(db.Integer, default=3)

    # Last error details
    last_error_message = db.Column(db.Text)
    last_error_details = db.Column(JSON)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    court = db.relationship("Court", back_populates="scraper_entries")

    def is_above_threshold(self):
        """Check if consecutive failures have reached the alert threshold."""
        return self.consecutive_failures >= self.failure_threshold

    def to_dict(self):
        """Serialize scraper registry entry to a dictionary."""
        return {
            "id": str(self.id),
            "court_code": self.court_code,
            "scraper_version": self.scraper_version,
            "is_healthy": self.is_healthy,
            "consecutive_failures": self.consecutive_failures,
            "total_runs": self.total_runs,
            "total_successes": self.total_successes,
            "total_failures": self.total_failures,
            "avg_parse_confidence": self.avg_parse_confidence,
            "last_run_at": self.last_run_at.isoformat() if self.last_run_at else None,
            "last_success_at": self.last_success_at.isoformat() if self.last_success_at else None,
            "last_failure_at": self.last_failure_at.isoformat() if self.last_failure_at else None,
            "last_error_message": self.last_error_message,
        }

    def __repr__(self):
        status = "healthy" if self.is_healthy else "unhealthy"
        return f"<ScraperRegistry {self.court_code} v{self.scraper_version} ({status})>"


class ScrapeLog(db.Model):
    """Audit trail of every scrape operation."""

    __tablename__ = "scrape_log"
    __table_args__ = {"extend_existing": True}

    # Valid statuses
    STATUSES = ("running", "success", "partial", "failed")

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    court_code = db.Column(db.String(30), db.ForeignKey("courts.code"), nullable=False)
    triggered_by = db.Column(db.String(50))
    triggered_by_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))

    # What was scraped
    source_url = db.Column(db.String(500))
    pdf_page_count = db.Column(db.Integer)
    cases_found = db.Column(db.Integer, default=0)
    cases_parsed_ok = db.Column(db.Integer, default=0)
    cases_parse_failed = db.Column(db.Integer, default=0)

    # Timing
    started_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    completed_at = db.Column(db.DateTime)
    duration_ms = db.Column(db.Integer)

    # Result
    status = db.Column(db.String(20), nullable=False, default="running")
    error_message = db.Column(db.Text)
    error_details = db.Column(JSON)

    # Confidence
    avg_parse_confidence = db.Column(db.Float)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    court = db.relationship("Court", back_populates="scrape_logs")

    def to_dict(self):
        """Serialize scrape log entry to a dictionary."""
        return {
            "id": str(self.id),
            "court_code": self.court_code,
            "triggered_by": self.triggered_by,
            "source_url": self.source_url,
            "cases_found": self.cases_found,
            "cases_parsed_ok": self.cases_parsed_ok,
            "cases_parse_failed": self.cases_parse_failed,
            "status": self.status,
            "duration_ms": self.duration_ms,
            "avg_parse_confidence": self.avg_parse_confidence,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message,
        }

    def __repr__(self):
        return f"<ScrapeLog {self.court_code} ({self.status})>"


class PdfFormatSignature(db.Model):
    """Known PDF format patterns per court. Detects when format changes."""

    __tablename__ = "pdf_format_signatures"
    __table_args__ = {"extend_existing": True}

    # Columns
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    court_code = db.Column(db.String(30), db.ForeignKey("courts.code"), nullable=False)

    # Format identification
    format_name = db.Column(db.String(100))
    format_version = db.Column(db.String(20))

    # Signature characteristics
    header_pattern = db.Column(db.Text)
    column_pattern = db.Column(ARRAY(db.Text))
    row_pattern = db.Column(db.Text)
    page_layout = db.Column(db.String(20))
    expected_columns = db.Column(db.Integer)

    # Sample data for validation
    sample_raw_text = db.Column(db.Text)

    # Status
    is_current = db.Column(db.Boolean, default=True)
    first_seen_at = db.Column(db.DateTime, server_default=db.func.now())
    last_seen_at = db.Column(db.DateTime, server_default=db.func.now())

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    court = db.relationship("Court", back_populates="pdf_signatures")

    def to_dict(self):
        """Serialize PDF format signature to a dictionary."""
        return {
            "id": str(self.id),
            "court_code": self.court_code,
            "format_name": self.format_name,
            "format_version": self.format_version,
            "page_layout": self.page_layout,
            "expected_columns": self.expected_columns,
            "is_current": self.is_current,
            "first_seen_at": self.first_seen_at.isoformat() if self.first_seen_at else None,
            "last_seen_at": self.last_seen_at.isoformat() if self.last_seen_at else None,
        }

    def __repr__(self):
        status = "current" if self.is_current else "archived"
        return f"<PdfFormatSignature {self.court_code}: {self.format_name} ({status})>"
