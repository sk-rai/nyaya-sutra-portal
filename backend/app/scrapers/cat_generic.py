"""Generic CAT (Central Administrative Tribunal) scraper.

Works for ALL CAT benches (Delhi/Principal, Mumbai, Chennai, Kolkata, etc.).
The court's base_url and cause_list_url are read from the courts table,
so this single scraper handles every CAT bench.

CAT cases can be appealed to High Courts, and HC cases can go to SC.
The case_relationships table tracks these linkages.
"""

import io
import logging
import re
from typing import List, Optional

from .base import BaseScraper, ScrapeResult
from .registry import register_scraper

logger = logging.getLogger(__name__)


@register_scraper
class CatGenericScraper(BaseScraper):
    """Generic scraper for all Central Administrative Tribunal benches.

    CAT benches publish cause lists as PDFs (similar format to AFT).
    URLs come from the courts table, making this scraper bench-agnostic.

    CAT → HC (appeal) → SC (SLP) linkage is tracked via case_relationships.

    Extracts: case_number, case_title, petitioner, respondent,
    advocate_petitioner, bench, item_number, next_hearing_date.
    """

    SCRAPER_KEY = "cat_generic"
    SCRAPER_VERSION = "1.0.0"
    COURT_TYPE = "cat"

    def fetch_pdf(self, court_code: str, case_number: str) -> Optional[bytes]:
        """Fetch cause list PDF for the given CAT bench.

        Looks up the court's cause_list_url from the database.

        Args:
            court_code: Court code (e.g., 'cat_del', 'cat_mum', 'cat_che').
            case_number: Case number (for logging context).

        Returns:
            Raw PDF bytes, or None if unavailable.
        """
        from ..extensions import db
        from ..models.court import Court

        court = Court.query.get(court_code)
        if not court:
            logger.error(f"[cat_generic] Court not found: {court_code}")
            return None

        fetch_url = court.cause_list_url or court.base_url
        if not fetch_url:
            logger.error(f"[cat_generic] No URL configured for court: {court_code}")
            return None

        try:
            response = self.session.get(fetch_url, timeout=self.REQUEST_TIMEOUT)
            response.raise_for_status()

            content = response.content

            # Direct PDF
            if content[:4] == b"%PDF":
                return content

            # HTML page — find PDF link
            if b"<html" in content[:1000].lower():
                pdf_url = self._find_pdf_link(
                    content.decode("utf-8", errors="ignore"),
                    court.base_url or fetch_url,
                )
                if pdf_url:
                    pdf_response = self.session.get(
                        pdf_url, timeout=self.REQUEST_TIMEOUT
                    )
                    pdf_response.raise_for_status()
                    if pdf_response.content[:4] == b"%PDF":
                        return pdf_response.content

            logger.warning(
                f"[cat_generic] Could not find PDF for {court_code} at {fetch_url}"
            )
            return None

        except Exception as e:
            logger.error(f"[cat_generic] Fetch failed for {court_code}: {e}")
            raise

    def _find_pdf_link(self, html: str, base_url: str) -> Optional[str]:
        """Extract cause list PDF link from HTML page."""
        # CAT sites often have "Daily Cause List" or "Supplementary" links
        patterns = [
            re.compile(r'href=["\']([^"\']*(?:cause|daily|list)[^"\']*\.pdf)["\']', re.IGNORECASE),
            re.compile(r'href=["\']([^"\']*\.pdf)["\']', re.IGNORECASE),
        ]

        for pattern in patterns:
            matches = pattern.findall(html)
            if matches:
                pdf_path = matches[0]
                if pdf_path.startswith("http"):
                    return pdf_path
                elif pdf_path.startswith("/"):
                    from urllib.parse import urlparse
                    parsed = urlparse(base_url)
                    return f"{parsed.scheme}://{parsed.netloc}{pdf_path}"
                else:
                    return f"{base_url.rstrip('/')}/{pdf_path}"

        return None

    def parse(self, raw_content: bytes) -> List[ScrapeResult]:
        """Parse CAT cause list PDF into structured case data.

        Args:
            raw_content: Raw PDF bytes.

        Returns:
            List of ScrapeResult objects.
        """
        try:
            import pdfplumber
        except ImportError:
            logger.error("[cat_generic] pdfplumber not installed")
            return []

        results = []

        try:
            with pdfplumber.open(io.BytesIO(raw_content)) as pdf:
                bench_name = self._extract_bench_info(pdf)

                for page_num, page in enumerate(pdf.pages, start=1):
                    tables = page.extract_tables()

                    if tables:
                        for table in tables:
                            parsed = self._parse_table(table, page_num, bench_name)
                            results.extend(parsed)
                    else:
                        text = page.extract_text()
                        if text:
                            parsed = self._parse_text(text, page_num, bench_name)
                            results.extend(parsed)

        except Exception as e:
            logger.error(f"[cat_generic] PDF parse error: {e}", exc_info=True)

        return results

    def _extract_bench_info(self, pdf) -> str:
        """Extract bench/court name from PDF header."""
        try:
            first_text = pdf.pages[0].extract_text() or ""
            # Look for bench patterns
            patterns = [
                re.compile(r"((?:principal|circuit)\s+bench[^,\n]*)", re.IGNORECASE),
                re.compile(r"(CAT[^,\n]*bench[^,\n]*)", re.IGNORECASE),
                re.compile(r"(Central Administrative Tribunal[^,\n]*)", re.IGNORECASE),
            ]
            for pattern in patterns:
                match = pattern.search(first_text)
                if match:
                    return match.group(1).strip()
        except Exception:
            pass
        return ""

    def _parse_table(
        self, table: list, page_num: int, bench_name: str
    ) -> List[ScrapeResult]:
        """Parse a table from the cause list."""
        results = []

        if not table or len(table) < 2:
            return results

        header = [str(c).strip().lower() if c else "" for c in table[0]]
        col_map = self._map_columns(header)

        for row in table[1:]:
            if not row or all(not cell for cell in row):
                continue
            result = self._row_to_result(row, col_map, page_num, bench_name)
            if result:
                results.append(result)

        return results

    def _map_columns(self, header: list) -> dict:
        """Map header labels to column indices for CAT format."""
        col_map = {}
        for idx, cell in enumerate(header):
            cl = cell.lower()
            if any(k in cl for k in ["item", "sr", "sl", "s.no", "sno"]):
                col_map["item_no"] = idx
            elif any(k in cl for k in ["case no", "case_no", "oa no", "application"]):
                col_map["case_no"] = idx
            elif any(k in cl for k in ["parties", "title", "applicant", "name"]):
                col_map["parties"] = idx
            elif "petitioner" in cl and "adv" in cl:
                col_map["adv_pet"] = idx
            elif "respondent" in cl and "adv" in cl:
                col_map["adv_res"] = idx
            elif any(k in cl for k in ["adv", "counsel", "advocate"]):
                if "adv_pet" not in col_map:
                    col_map["adv_pet"] = idx
            elif any(k in cl for k in ["remark", "status", "order", "result"]):
                col_map["remarks"] = idx
            elif any(k in cl for k in ["date", "hearing", "next"]):
                col_map["next_date"] = idx
            elif any(k in cl for k in ["bench", "court", "hon"]):
                col_map["bench"] = idx
        return col_map

    def _row_to_result(
        self, row: list, col_map: dict, page_num: int, bench_name: str
    ) -> Optional[ScrapeResult]:
        """Convert a table row to a ScrapeResult."""
        def cell(field):
            idx = col_map.get(field)
            if idx is not None and idx < len(row):
                return str(row[idx]).strip() if row[idx] else ""
            return ""

        case_number = cell("case_no")
        if not case_number:
            return None

        parties_text = cell("parties")
        petitioner, respondent = self._split_parties(parties_text)

        row_bench = cell("bench") or bench_name

        structured = {
            "case_number": case_number,
            "case_title": parties_text,
            "petitioner": petitioner,
            "respondent": respondent,
            "advocate_petitioner": cell("adv_pet"),
            "advocate_respondent": cell("adv_res"),
            "item_number": cell("item_no"),
            "bench": row_bench,
            "next_hearing_date": cell("next_date"),
            "remarks": cell("remarks"),
        }

        parse_errors = []
        filled = sum(1 for v in structured.values() if v)
        confidence = filled / len(structured)

        raw_row = " | ".join(str(c) for c in row if c)

        return ScrapeResult(
            structured=structured,
            raw_data=raw_row,
            confidence=confidence,
            parse_errors=parse_errors,
            extra_fields={},
            source_url="",
            source_page=page_num,
        )

    def _parse_text(
        self, text: str, page_num: int, bench_name: str
    ) -> List[ScrapeResult]:
        """Fallback: parse plain text using regex."""
        results = []

        # CAT case number patterns: OA/123/2024, MA/456/2023, etc.
        case_pattern = re.compile(
            r"((?:OA|MA|TA|RA|CP|AT)\s*(?:No\.?\s*)?[\d/]+\d{4})",
            re.IGNORECASE,
        )

        for match in case_pattern.finditer(text):
            case_number = match.group(1).strip()
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
                "bench": bench_name,
                "next_hearing_date": "",
                "remarks": "",
            }

            results.append(ScrapeResult(
                structured=structured,
                raw_data=context,
                confidence=0.35,
                parse_errors=["text_only_extraction"],
                extra_fields={"extraction_method": "regex"},
                source_url="",
                source_page=page_num,
            ))

        return results

    def _split_parties(self, text: str) -> tuple:
        """Split 'Petitioner vs Respondent' text."""
        if not text:
            return ("", "")
        for sep in [" vs ", " v/s ", " versus ", " Vs ", " V/S ", " VS ", " v. "]:
            if sep in text:
                parts = text.split(sep, 1)
                return (parts[0].strip(), parts[1].strip())
        return (text.strip(), "")
