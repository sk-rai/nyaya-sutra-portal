"""Base scraper abstract class for the Nyaya Sutra Backend.

Defines the scraping pipeline: fetch → parse → store.
All court-specific scrapers extend this class.
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


@dataclass
class ScrapeResult:
    """Result of a scrape operation.

    Attributes:
        structured: Parsed structured data (case fields).
        raw_data: Raw text/content preserved for re-parsing.
        confidence: Parse confidence score [0.0, 1.0].
        parse_errors: List of fields that failed to parse.
        extra_fields: Additional extracted data not in standard schema.
        source_url: URL the data was fetched from.
        source_page: Page number in PDF (if applicable).
    """

    structured: Dict[str, Any] = field(default_factory=dict)
    raw_data: str = ""
    confidence: float = 0.0
    parse_errors: List[str] = field(default_factory=list)
    extra_fields: Dict[str, Any] = field(default_factory=dict)
    source_url: str = ""
    source_page: Optional[int] = None

    def __post_init__(self):
        """Ensure confidence is within bounds."""
        self.confidence = max(0.0, min(1.0, self.confidence))


class BaseScraper(ABC):
    """Abstract base class for all court scrapers.

    Subclasses must implement:
        - fetch_pdf(court_code, case_number): Fetch raw content from court website
        - parse(raw_content): Parse raw content into structured data

    Provides concrete methods:
        - scrape(court_code, case_number): Full pipeline (fetch → parse → result)
        - detect_format(raw_content): Identify PDF format signature
        - update_health(court_code, success, confidence): Update scraper health metrics
    """

    # Scraper metadata — override in subclasses
    SCRAPER_KEY = "base"
    SCRAPER_VERSION = "1.0.0"
    COURT_TYPE = "generic"

    # Request configuration
    REQUEST_TIMEOUT = 30  # seconds
    USER_AGENT = "NyayaSutra/1.0 (Legal Case Tracker)"

    def __init__(self):
        """Initialize the scraper with a requests session."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.USER_AGENT,
        })

    @abstractmethod
    def fetch_pdf(self, court_code: str, case_number: str) -> Optional[bytes]:
        """Fetch raw PDF/content from the court website.

        Args:
            court_code: Court identifier (e.g., 'aft_del').
            case_number: Case number to search for.

        Returns:
            Raw bytes of the PDF/page content, or None if not found.

        Raises:
            Exception: On network or access errors.
        """
        pass

    @abstractmethod
    def parse(self, raw_content: bytes) -> List[ScrapeResult]:
        """Parse raw content into structured case data.

        Args:
            raw_content: Raw bytes from fetch_pdf.

        Returns:
            List of ScrapeResult objects (one per case found in the document).
        """
        pass

    def scrape(self, court_code: str, case_number: str) -> Optional[ScrapeResult]:
        """Execute the full scraping pipeline.

        Fetch → Parse → Find matching case → Log → Return result.

        Args:
            court_code: Court identifier.
            case_number: Case number to search for.

        Returns:
            ScrapeResult for the matching case, or None if not found.
        """
        start_time = time.time()

        try:
            # Fetch
            raw_content = self.fetch_pdf(court_code, case_number)
            if raw_content is None:
                logger.warning(
                    f"[{self.SCRAPER_KEY}] No content fetched for "
                    f"{court_code}/{case_number}"
                )
                self.update_health(court_code, success=False, confidence=0.0)
                return None

            # Parse
            results = self.parse(raw_content)

            if not results:
                logger.info(
                    f"[{self.SCRAPER_KEY}] No cases parsed from "
                    f"{court_code}/{case_number}"
                )
                self.update_health(court_code, success=True, confidence=0.0)
                return None

            # Find matching case
            matching = self._find_matching_case(results, case_number)

            if matching:
                # Log confidence warning
                if matching.confidence < 0.7:
                    logger.warning(
                        f"[{self.SCRAPER_KEY}] Low confidence ({matching.confidence:.2f}) "
                        f"for {court_code}/{case_number}"
                    )

                self.update_health(
                    court_code, success=True, confidence=matching.confidence
                )
            else:
                # Parsed content but no match for this case number
                logger.info(
                    f"[{self.SCRAPER_KEY}] Case {case_number} not found in "
                    f"parsed results for {court_code}"
                )
                self.update_health(court_code, success=True, confidence=0.0)

            elapsed_ms = int((time.time() - start_time) * 1000)
            logger.info(
                f"[{self.SCRAPER_KEY}] Scrape complete for {court_code}/{case_number} "
                f"in {elapsed_ms}ms (results={len(results)}, match={'yes' if matching else 'no'})"
            )

            return matching

        except requests.RequestException as e:
            logger.error(
                f"[{self.SCRAPER_KEY}] Network error for {court_code}/{case_number}: {e}"
            )
            self.update_health(
                court_code, success=False, confidence=0.0, error=str(e)
            )
            return None

        except Exception as e:
            logger.error(
                f"[{self.SCRAPER_KEY}] Unexpected error for {court_code}/{case_number}: {e}",
                exc_info=True,
            )
            self.update_health(
                court_code, success=False, confidence=0.0, error=str(e)
            )
            return None

    def _find_matching_case(
        self, results: List[ScrapeResult], case_number: str
    ) -> Optional[ScrapeResult]:
        """Find the result matching the requested case number.

        Args:
            results: List of parsed results.
            case_number: Case number to match.

        Returns:
            Matching ScrapeResult or None.
        """
        case_number_normalized = case_number.strip().lower().replace(" ", "")

        for result in results:
            parsed_number = (
                result.structured.get("case_number", "")
                .strip()
                .lower()
                .replace(" ", "")
            )
            if parsed_number == case_number_normalized:
                return result

        # Fuzzy match: check if case_number is contained in any result
        for result in results:
            parsed_number = (
                result.structured.get("case_number", "")
                .strip()
                .lower()
                .replace(" ", "")
            )
            if case_number_normalized in parsed_number or parsed_number in case_number_normalized:
                return result

        return None

    def detect_format(self, raw_content: bytes) -> Optional[str]:
        """Detect the PDF format signature from raw content.

        Override in subclasses for court-specific format detection.

        Args:
            raw_content: Raw bytes of the document.

        Returns:
            Format identifier string, or None if unknown.
        """
        # Default: check if it's a PDF
        if raw_content[:4] == b"%PDF":
            return "pdf"
        elif b"<html" in raw_content[:1000].lower():
            return "html"
        return None

    def update_health(
        self,
        court_code: str,
        success: bool,
        confidence: float,
        error: Optional[str] = None,
    ) -> None:
        """Update scraper health metrics in the database.

        On success:
            - Reset consecutive_failures to 0
            - Update last_success_at
            - Update avg_parse_confidence (rolling average)

        On failure:
            - Increment consecutive_failures
            - Update last_failure_at
            - Store error details
            - If consecutive_failures >= failure_threshold → set is_healthy=False

        Args:
            court_code: Court identifier.
            success: Whether the scrape succeeded.
            confidence: Parse confidence score [0.0, 1.0].
            error: Error message (on failure).
        """
        try:
            from ..extensions import db
            from ..models.scraper import ScraperRegistry

            registry = ScraperRegistry.query.filter_by(
                court_code=court_code,
                scraper_version=self.SCRAPER_VERSION,
            ).first()

            if not registry:
                # Create new registry entry
                registry = ScraperRegistry(
                    court_code=court_code,
                    scraper_version=self.SCRAPER_VERSION,
                    consecutive_failures=0,
                    total_runs=0,
                    total_successes=0,
                    total_failures=0,
                    is_healthy=True,
                )
                db.session.add(registry)

            now = datetime.now(timezone.utc)
            registry.last_run_at = now
            registry.total_runs = (registry.total_runs or 0) + 1

            if success:
                registry.consecutive_failures = 0
                registry.last_success_at = now
                registry.total_successes = (registry.total_successes or 0) + 1
                registry.is_healthy = True

                # Update rolling average confidence
                if confidence > 0:
                    if registry.avg_parse_confidence is None:
                        registry.avg_parse_confidence = confidence
                    else:
                        # Exponential moving average (alpha=0.3)
                        alpha = 0.3
                        registry.avg_parse_confidence = (
                            alpha * confidence
                            + (1 - alpha) * registry.avg_parse_confidence
                        )
            else:
                registry.consecutive_failures = (registry.consecutive_failures or 0) + 1
                registry.last_failure_at = now
                registry.total_failures = (registry.total_failures or 0) + 1
                registry.last_error_message = error

                # Check threshold
                if registry.consecutive_failures >= registry.failure_threshold:
                    registry.is_healthy = False
                    logger.warning(
                        f"[{self.SCRAPER_KEY}] Scraper for {court_code} marked UNHEALTHY "
                        f"({registry.consecutive_failures} consecutive failures)"
                    )

            db.session.commit()

        except Exception as e:
            logger.error(
                f"[{self.SCRAPER_KEY}] Failed to update health for {court_code}: {e}"
            )
            # Don't let health update failures break the scraping pipeline
            try:
                from ..extensions import db
                db.session.rollback()
            except Exception:
                pass
