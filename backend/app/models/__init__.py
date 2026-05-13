"""SQLAlchemy models for the Nyaya Sutra Backend API.

All models map to existing PostgreSQL tables (no migrations needed).
Import all models here so they are registered with SQLAlchemy's metadata
when the application starts.
"""

from .case import CaseCache, CaseHearing, CaseRelationship
from .court import Court
from .otp import OTPToken
from .scraper import PdfFormatSignature, ScrapeLog, ScraperRegistry
from .subscription import Subscription
from .tracking import UserTrackedCase
from .user import User, UserSession

__all__ = [
    "Court",
    "User",
    "UserSession",
    "CaseCache",
    "CaseHearing",
    "CaseRelationship",
    "Subscription",
    "OTPToken",
    "UserTrackedCase",
    "ScraperRegistry",
    "ScrapeLog",
    "PdfFormatSignature",
]
