"""Fallback generic parser for the Nyaya Sutra Backend.

Used when no court-specific scraper exists. Attempts generic PDF text
extraction using pdfplumber and regex patterns to extract common fields.

Sets lower parse_confidence (0.3-0.5) and flags results for admin review.
Works for any court type (HC, SC, AFT, CAT, District, etc.).
"""

import io
import logging
import re
from typing import List, Optional

from .base import BaseScraper, ScrapeResult
from .registry import register_scraper

logger = logging.getLogger(__name__)


@register_scraper
class FallbackScraper(BaseScraper):
    """Generic fallback scraper for any court without a specific parser.

    Attempts to extract case information using:
    1. pdfplumber table extraction
    2. Regex patterns for common case number formats
    3. Heuristic party name splitting

    Results have lower confidence (0.3-0.5) and are flagged for admin review.
    """

    SCRAPER_KEY = "fallback"
    SCRAPER_VERSION = "1.0.0"
    COURT_TYPE = "generic"

    # Common case number patterns across Indian courts
    CASE_PATTERNS = [
        # AFT/CAT: OA 123/2024, TA 456/2023, MA 789/2022
        re.compile(r"((?:OA|TA|MA|RA|CA|AP|CP|AT)\s*(?:No\.?\s*)?[\d/]+\d{4})", re.IGNORECASE),
        # HC: WP(C) 123/2024, CRL.A. 456/2023
        re.compile(r"((?:WP|CRL|SLP|CMP|RP|FAO|RSA|SA|CS|OS)\s*\(?[A-Z]*\)?\s*(?:No\.?\s*)?[\d/]+\d{4})", re.IGNORECASE),
        # SC: SLP(C) 123/2024, Civil Appeal 456/2023
        re.compile(r"((?:Civil|Criminal)\s+(?:Appeal|Petition)\s*(?:No\.?\s*)?[\d/]+\d{4})", re.IGNORECASE),
        # Generic: Any "No. 123/2024" pattern
        re.compile(r"((?:Case|Petition|Appeal|Application)\s*No\.?\s*[\d/]+\d{4})", re.IGNORECASE),
    ]

    def fetch_pdf(self, court_code: str, case_number: str) -> Optional[bytes]:
        """Fetch content from the court's configured URL.

        Args:
            court_code: Court code from the courts table.
            case_number: Case number (for logging).

        Returns:
            Raw content bytes, or None.
        """
        from ..extensions import db
        from ..models.court import Court

        court = Court.query.get(court_code)
        if not court:
            logger.error(f"[fallback] Court not found: {court_code}")
            return None

        fetch_url = court.cause_list_url or court.base_url
        if not fetch_url:
            logger.error(f"[fallback] No URL configured for court: {court_code}")
            return None

        try:
            response = self.session.get(fetch_url, timeout=self.REQUEST_TIMEOUT)
            response.raise_for_status()

            content = response.content

            # Direct PDF
            if content[:4] == b"%PDF":
                return content

            # HTML — try to find PDF links
            if b"<html" in content[:1000].lower():
                pdf_url = self._find_any_pdf_link(
                    content.decode("utf-8", errors="ignore"),
                    court.base_url or fetch_url,
                )
                if pdf_url:
                    pdf_resp = self.session.get(pdf_url, timeout=self.REQUEST_TIMEOUT)
                    pdf_resp.raise_for_status()
                    if pdf_resp.content[:4] == b"%PDF":
                        return pdf_resp.content

            # Return HTML content as-is for text parsing
            return content

        except Exception as e:
            logger.error(f"[fallback] Fetch failed for {court_code}: {e}")
            raise

    def _find_any_pdf_link(self, html: str, base_url: str) -> Optional[str]:
        """Find any PDF link in the HTML."""
        pattern = re.compile(r'href=["\']([^"\']*\.pdf)["\']', re.IGNORECASE)
        matches = pattern.findall(html)

        if not matches:
            return None

        pdf_path = matches[0]
        if pdf_path.startswith("http"):
            return pdf_path
        elif pdf_path.startswith("/"):
            from urllib.parse import urlparse
            parsed = urlparse(base_url)
            return f"{parsed.scheme}://{parsed.netloc}{pdf_path}"
        else:
            return f"{base_url.rstrip('/')}/{pdf_path}"

    def parse(self, raw_content: bytes) -> List[ScrapeResult]:
        """Parse content using generic strategies.

        Tries PDF table extraction first, then text regex patterns.

        Args:
            raw_content: Raw content bytes (PDF or HTML).

        Returns:
            List of ScrapeResult objects with lower confidence.
        """
        # Try PDF parsing
        if raw_content[:4] == b"%PDF":
            return self._parse_pdf(raw_content)

        # Try HTML/text parsing
        try:
            text = raw_content.decode("utf-8", errors="ignore")
            return self._parse_html_text(text)
        except Exception as e:
            logger.error(f"[fallback] Parse error: {e}")
            return []

    def _parse_pdf(self, raw_content: bytes) -> List[ScrapeResult]:
        """Parse PDF using pdfplumber with generic extraction."""
        try:
            import pdfplumber
        except ImportError:
            logger.error("[fallback] pdfplumber not installed")
            return []

        results = []

        try:
            with pdfplumber.open(io.BytesIO(raw_content)) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    # Try tables first
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            parsed = self._parse_generic_table(table, page_num)
                            results.extend(parsed)
                    else:
                        # Fall back to text
                        text = page.extract_text()
                        if text:
                            parsed = self._extract_cases_from_text(text, page_num)
                            results.extend(parsed)

        except Exception as e:
            logger.error(f"[fallback] PDF parse error: {e}", exc_info=True)

        # Flag all results for admin review
        for result in results:
            result.extra_fields["needs_review"] = True
            result.extra_fields["parser"] = "fallback"

        return results

    def _parse_generic_table(self, table: list, page_num: int) -> List[ScrapeResult]:
        """Attempt to parse any table format generically."""
        results = []

        if not table or len(table) < 2:
            return results

        # Try to identify which column has case numbers
        header = [str(c).strip().lower() if c else "" for c in table[0]]
        case_col = None

        for idx, h in enumerate(header):
            if any(k in h for k in ["case", "no", "number", "oa", "wp", "slp"]):
                case_col = idx
                break

        # If no header match, scan rows for case number patterns
        if case_col is None:
            case_col = self._detect_case_column(table[1:])

        if case_col is None:
            return results

        for row in table[1:]:
            if not row or case_col >= len(row):
                continue

            case_number = str(row[case_col]).strip() if row[case_col] else ""
            if not case_number or len(case_number) < 3:
                continue

            # Gather all other cells as context
            other_cells = [str(c).strip() for i, c in enumerate(row) if i != case_col and c]
            parties_text = " ".join(other_cells[:2]) if other_cells else ""

            petitioner, respondent = self._split_parties(parties_text)

            structured = {
                "case_number": case_number,
                "case_title": parties_text,
                "petitioner": petitioner,
                "respondent": respondent,
                "advocate_petitioner": "",
                "advocate_respondent": "",
                "item_number": "",
                "bench": "",
                "next_hearing_date": "",
                "remarks": "",
            }

            raw_row = " | ".join(str(c) for c in row if c)

            results.append(ScrapeResult(
                structured=structured,
                raw_data=raw_row,
                confidence=0.4,
                parse_errors=["generic_table_extraction"],
                extra_fields={"needs_review": True, "parser": "fallback"},
                source_url="",
                source_page=page_num,
            ))

        return results

    def _detect_case_column(self, rows: list) -> Optional[int]:
        """Detect which column contains case numbers by scanning data rows."""
        if not rows:
            return None

        # Check each column for case number patterns
        max_cols = max(len(row) for row in rows if row)
        for col_idx in range(max_cols):
            matches = 0
            for row in rows[:10]:  # Check first 10 rows
                if row and col_idx < len(row) and row[col_idx]:
                    cell = str(row[col_idx])
                    for pattern in self.CASE_PATTERNS:
                        if pattern.search(cell):
                            matches += 1
                            break
            if matches >= 2:  # At least 2 matches in first 10 rows
                return col_idx

        return None

    def _extract_cases_from_text(self, text: str, page_num: int) -> List[ScrapeResult]:
        """Extract case numbers from plain text using regex patterns."""
        results = []
        seen_cases = set()

        for pattern in self.CASE_PATTERNS:
            for match in pattern.finditer(text):
                case_number = match.group(1).strip()

                # Deduplicate
                if case_number.lower() in seen_cases:
                    continue
                seen_cases.add(case_number.lower())

                # Extract context
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 150)
                context = text[start:end]

                structured = {
                    "case_number": case_number,
                    "case_title": "",
                    "petitioner": "",
                    "respondent": "",
                    "advocate_petitioner": "",
                    "advocate_respondent": "",
                    "item_number": "",
                    "bench": "",
                    "next_hearing_date": "",
                    "remarks": "",
                }

                results.append(ScrapeResult(
                    structured=structured,
                    raw_data=context,
                    confidence=0.3,
                    parse_errors=["text_only_extraction", "fallback_parser"],
                    extra_fields={"needs_review": True, "parser": "fallback"},
                    source_url="",
                    source_page=page_num,
                ))

        return results

    def _parse_html_text(self, html: str) -> List[ScrapeResult]:
        """Parse HTML content for case information."""
        # Strip HTML tags for text extraction
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text)

        return self._extract_cases_from_text(text, page_num=1)

    def _split_parties(self, text: str) -> tuple:
        """Split parties text."""
        if not text:
            return ("", "")
        for sep in [" vs ", " v/s ", " versus ", " Vs ", " V/S ", " VS ", " v. "]:
            if sep in text:
                parts = text.split(sep, 1)
                return (parts[0].strip(), parts[1].strip())
        return (text.strip(), "")
