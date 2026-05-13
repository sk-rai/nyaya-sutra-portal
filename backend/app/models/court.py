"""Court model mapping to the existing 'courts' table."""

from ..extensions import db


class Court(db.Model):
    """Reference table of all supported courts.

    This is a static/manually-maintained table. The primary key is a
    short string code (e.g., 'sc', 'hc_del', 'aft_del').
    """

    __tablename__ = "courts"
    __table_args__ = {"extend_existing": True}

    # Valid court types
    COURT_TYPES = ("sc", "hc", "aft", "cat", "district", "appellate")

    # Columns
    code = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(50))
    court_type = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    base_url = db.Column(db.String(500))
    cause_list_url = db.Column(db.String(500))
    scraper_key = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    cases = db.relationship("CaseCache", back_populates="court", lazy="dynamic")
    scraper_entries = db.relationship("ScraperRegistry", back_populates="court", lazy="dynamic")
    scrape_logs = db.relationship("ScrapeLog", back_populates="court", lazy="dynamic")
    pdf_signatures = db.relationship("PdfFormatSignature", back_populates="court", lazy="dynamic")

    def to_dict(self):
        """Serialize court to a dictionary for API responses."""
        return {
            "code": self.code,
            "name": self.name,
            "short_name": self.short_name,
            "court_type": self.court_type,
            "state": self.state,
            "city": self.city,
            "base_url": self.base_url,
            "cause_list_url": self.cause_list_url,
            "scraper_key": self.scraper_key,
            "is_active": self.is_active,
        }

    def __repr__(self):
        return f"<Court {self.code}: {self.short_name or self.name}>"
