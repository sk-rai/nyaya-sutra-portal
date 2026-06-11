"""Generic AFT (Armed Forces Tribunal) scraper.

Rewritten to handle the REAL AFT cause list PDF format which uses
text-based columnar layout (NOT grid tables). The format is:

    ARMED FORCES TRIBUNAL, PRINCIPAL BENCH, NEW DELHI
    LIST OF BUSINESS
    Date: DD-MM-YYYY
    COURT No. X
    CORAM: HON'BLE [JUDGES]

    S.No  Case No.  Parties Name  Advocate for Petitioner / Respondents
    CATEGORY HEADING (e.g., ADMISSION MATTERS, FOR FINAL HEARING)
    1.  OA 750/2026  Petitioner Name V/s Respondent  Adv Pet / Adv Res

Works for ALL AFT benches. URLs come from the courts table.
"""

import io
import logging
import re
from typing import List, Optional, Tuple

from .base import BaseScraper, ScrapeResult
from .registry import register_scraper

logger = logging.getLogger(__name__)


@register_scraper
class AftGenericScraper(BaseScraper):
    """Generic scraper for all Armed Forces Tribunal benches.

    Parses the text-based cause list PDF format used by AFT.
    Handles multiple courts within a single PDF.
    """

    SCRAPER_KEY = "aft_generic"
    SCRAPER_VERSION = "2.0.0"
    COURT_TYPE = "aft"

    # Case number patterns for AFT
    CASE_PATTERN = re.compile(
        r"((?:OA|TA|MA|RA|WP|CA)\s+\d+/\d{4})",
        re.IGNORECASE,
    )

    # Pattern for serial number at start of a case entry
    SERIAL_PATTERN = re.compile(
        r"^(\d+)\.\s+",
        re.MULTILINE,
    )

    def fetch_pdf(self, court_code: str, case_number: str) -> Optional[bytes]:
        """Fetch cause list PDF for the given AFT bench.

        Looks up the court's cause_list_url from the database.
        Handles expired SSL certificates (common on .nic.in sites).
        """
        from ..extensions import db
        from ..models.court import Court

        court = Court.query.get(court_code)
        if not court:
            logger.error(f"[aft] Court not found: {court_code}")
            return None

        fetch_url = court.cause_list_url or court.base_url
        if not fetch_url:
            logger.error(f"[aft] No URL configured for court: {court_code}")
            return None

        try:
            # Disable SSL verification for .nic.in sites (often have expired certs)
            verify_ssl = not fetch_url.endswith(".nic.in") and "nic.in" not in fetch_url
            response = self.session.get(
                fetch_url, timeout=self.REQUEST_TIMEOUT, verify=verify_ssl
            )
            response.raise_for_status()
            content = response.content

            # Direct PDF
            if content[:4] == b"%PDF":
                return content

            # HTML page — find PDF links
            if b"<html" in content[:2000].lower() or b"<!doctype" in content[:500].lower():
                pdf_url = self._find_pdf_link(
                    content.decode("utf-8", errors="ignore"),
                    court.base_url or fetch_url,
                )
                if pdf_url:
                    pdf_response = self.session.get(
                        pdf_url, timeout=self.REQUEST_TIMEOUT, verify=verify_ssl
                    )
                    pdf_response.raise_for_status()
                    if pdf_response.content[:4] == b"%PDF":
                        return pdf_response.content

            logger.warning(f"[aft] Could not find PDF for {court_code} at {fetch_url}")
            return None

        except Exception as e:
            logger.error(f"[aft] Fetch failed for {court_code}: {e}")
            raise

    def _find_pdf_link(self, html: str, base_url: str) -> Optional[str]:
        """Extract cause list PDF link from HTML page."""
        from urllib.parse import urlparse

        # Look for cause list / daily list PDF links
        patterns = [
            re.compile(r'href=["\']([^"\']*(?:cause|daily|list)[^"\']*\.pdf)["\']', re.IGNORECASE),
            re.compile(r'href=["\']([^"\']*\.pdf)["\']', re.IGNORECASE),
        ]

        for pattern in patterns:
            matches = pattern.findall(html)
            if matches:
                # Take the first (most recent) match
                pdf_path = matches[0]
                if pdf_path.startswith("http"):
                    return pdf_path
                elif pdf_path.startswith("/"):
                    parsed = urlparse(base_url)
                    return f"{parsed.scheme}://{parsed.netloc}{pdf_path}"
                else:
                    return f"{base_url.rstrip('/')}/{pdf_path}"

        return None

    def parse(self, raw_content: bytes) -> List[ScrapeResult]:
        """Parse AFT cause list PDF using text extraction.

        The real AFT PDF format is text-based (not table-grid).
        We extract text page by page and parse using regex patterns.
        """
        try:
            import pdfplumber
        except ImportError:
            logger.error("[aft] pdfplumber not installed")
            return []

        results = []

        try:
            with pdfplumber.open(io.BytesIO(raw_content)) as pdf:
                # Extract all text from the PDF
                full_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n\n"

                if not full_text.strip():
                    logger.warning("[aft] No text extracted from PDF")
                    return []

                # Parse the full text
                results = self._parse_full_text(full_text)

        except Exception as e:
            logger.error(f"[aft] PDF parse error: {e}", exc_info=True)

        logger.info(f"[aft] Parsed {len(results)} cases from PDF")
        return results

    def _parse_full_text(self, text: str) -> List[ScrapeResult]:
        """Parse the full extracted text into case results.

        Strategy:
        1. Split by court sections (COURT No. X headers)
        2. For each court section, extract bench/coram info
        3. Split into individual case entries by serial numbers
        4. Parse each case entry for case number, parties, advocates
        """
        results = []

        # Split into court sections
        court_sections = self._split_into_courts(text)

        for court_info, section_text in court_sections:
            # Parse individual cases from this court section
            cases = self._parse_court_section(section_text, court_info)
            results.extend(cases)

        return results

    def _split_into_courts(self, text: str) -> List[Tuple[dict, str]]:
        """Split the PDF text into sections per court/bench.

        Returns list of (court_info_dict, section_text) tuples.
        """
        # Pattern to match court headers
        court_header_pattern = re.compile(
            r"COURT\s+No\.\s*(\d+)\s*\([^)]*\)",
            re.IGNORECASE,
        )

        # Find all court headers
        splits = list(court_header_pattern.finditer(text))

        if not splits:
            # Single court or no header found — treat entire text as one section
            bench = self._extract_coram(text)
            date = self._extract_date(text)
            return [({
                "court_number": "1",
                "bench": bench,
                "date": date,
            }, text)]

        sections = []
        for i, match in enumerate(splits):
            start = match.start()
            end = splits[i + 1].start() if i + 1 < len(splits) else len(text)
            section_text = text[start:end]

            court_number = match.group(1)
            bench = self._extract_coram(section_text)
            date = self._extract_date(text[:500])  # Date is usually at the top

            sections.append(({
                "court_number": court_number,
                "bench": bench,
                "date": date,
            }, section_text))

        return sections

    def _extract_coram(self, text: str) -> str:
        """Extract bench/coram (judge names) from section text."""
        coram_pattern = re.compile(
            r"CORAM:\s*\n?(.*?)(?:\n\s*S\.\s*No|$)",
            re.IGNORECASE | re.DOTALL,
        )
        match = coram_pattern.search(text[:1000])
        if match:
            coram = match.group(1).strip()
            # Clean up — take the HON'BLE lines
            lines = [l.strip() for l in coram.split("\n") if "HON" in l.upper()]
            return " & ".join(lines) if lines else coram[:200]
        return ""

    def _extract_date(self, text: str) -> str:
        """Extract the cause list date."""
        date_pattern = re.compile(
            r"Date:\s*(\d{2}-\d{2}-\d{4})",
            re.IGNORECASE,
        )
        match = date_pattern.search(text)
        return match.group(1) if match else ""

    def _parse_court_section(
        self, text: str, court_info: dict
    ) -> List[ScrapeResult]:
        """Parse all cases from one court section.

        Uses the pattern: serial number followed by case details
        ending at the next serial number or section end.
        """
        results = []

        # Find all case entries by serial number pattern
        # Pattern: line starting with "number." possibly with whitespace
        entry_pattern = re.compile(
            r"(?:^|\n)\s*(\d+)\.\s+",
        )

        entries = list(entry_pattern.finditer(text))

        if not entries:
            return results

        for i, match in enumerate(entries):
            start = match.start()
            end = entries[i + 1].start() if i + 1 < len(entries) else len(text)
            entry_text = text[start:end].strip()
            serial_no = match.group(1)

            # Parse this individual case entry
            case_result = self._parse_case_entry(entry_text, serial_no, court_info)
            if case_result:
                results.append(case_result)

        return results

    def _parse_case_entry(
        self, entry_text: str, serial_no: str, court_info: dict
    ) -> Optional[ScrapeResult]:
        """Parse a single case entry block into a ScrapeResult.

        A typical entry looks like:
            1.  OA 750/2026  No 15707752-L Ex Hav Manphool Singh
                             V/s
                             UOI & Ors.
                                                    Devendra Kumar /
                                                    Kuldeep Singh

        Or with "with" / "in" references:
            3.  MA 4086/2022   AVM Laxmi Narain Sharma...  Ajit Kakkar /
                with                                       Anil Gautam Sr CGSC
                MA 1145/2024
                in
                OA 1906/2020
        """
        # Extract the primary case number (first case number in the entry)
        case_numbers = self.CASE_PATTERN.findall(entry_text)
        if not case_numbers:
            return None

        primary_case = case_numbers[0].strip()

        # Related cases (with/in references)
        related_cases = case_numbers[1:] if len(case_numbers) > 1 else []

        # Extract petitioner and respondent
        petitioner, respondent = self._extract_parties(entry_text)

        # Extract advocates
        adv_petitioner, adv_respondent = self._extract_advocates(entry_text)

        # Determine case category from context
        category = self._detect_category(entry_text)

        # Build structured data
        structured = {
            "case_number": primary_case,
            "case_title": f"{petitioner} V/s {respondent}" if petitioner else "",
            "petitioner": petitioner,
            "respondent": respondent,
            "advocate_petitioner": adv_petitioner,
            "advocate_respondent": adv_respondent,
            "item_number": serial_no,
            "bench": court_info.get("bench", ""),
            "court_number": court_info.get("court_number", ""),
            "hearing_date": court_info.get("date", ""),
            "category": category,
            "related_cases": related_cases,
        }

        # Calculate confidence based on fields filled
        core_fields = ["case_number", "petitioner", "respondent", "advocate_petitioner"]
        filled_core = sum(1 for f in core_fields if structured.get(f))
        confidence = filled_core / len(core_fields)

        # Boost confidence if we have good data
        if petitioner and respondent and adv_petitioner:
            confidence = max(confidence, 0.85)

        parse_errors = []
        if not petitioner:
            parse_errors.append("petitioner_missing")
        if not adv_petitioner:
            parse_errors.append("advocate_missing")

        return ScrapeResult(
            structured=structured,
            raw_data=entry_text[:500],  # Keep first 500 chars of raw text
            confidence=confidence,
            parse_errors=parse_errors,
            extra_fields={
                "related_cases": related_cases,
                "category": category,
            },
            source_url="",
            source_page=0,
        )

    def _extract_parties(self, text: str) -> Tuple[str, str]:
        """Extract petitioner and respondent from case entry text.

        Pattern: Everything between case number and "V/s" is petitioner info.
        Everything after "V/s" until the advocate section is respondent.
        """
        # Find V/s separator
        vs_pattern = re.compile(r"\bV/s\b", re.IGNORECASE)
        vs_match = vs_pattern.search(text)

        if not vs_match:
            return ("", "")

        # Text before V/s — extract petitioner name
        before_vs = text[:vs_match.start()]
        # Remove serial number and case number from the beginning
        # The petitioner name typically comes after the case number
        case_match = self.CASE_PATTERN.search(before_vs)
        if case_match:
            petitioner_text = before_vs[case_match.end():].strip()
        else:
            petitioner_text = before_vs.strip()

        # Clean up petitioner — remove "with", "in", extra case numbers
        petitioner_lines = []
        for line in petitioner_text.split("\n"):
            line = line.strip()
            if line and not re.match(r"^(with|in|WITH|IN)$", line):
                # Skip lines that are just case numbers
                if not self.CASE_PATTERN.match(line):
                    petitioner_lines.append(line)

        petitioner = " ".join(petitioner_lines).strip()
        # Remove leading numbers/service numbers that might be part of name
        petitioner = re.sub(r"^\d+\.\s*", "", petitioner).strip()

        # Text after V/s — extract respondent
        after_vs = text[vs_match.end():]
        # Respondent is typically on the next line(s) until advocate names
        respondent_lines = []
        for line in after_vs.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Stop when we hit what looks like advocate names (contains "/")
            if "/" in line and not line.startswith("UOI"):
                break
            respondent_lines.append(line)
            # Usually respondent is just "UOI & Ors" or similar — 1-2 lines
            if len(respondent_lines) >= 2:
                break

        respondent = " ".join(respondent_lines).strip()

        return (petitioner[:300], respondent[:300])

    def _extract_advocates(self, text: str) -> Tuple[str, str]:
        """Extract advocate names for petitioner and respondent.

        In AFT format, advocates are listed as:
            "Adv Petitioner / Adv Respondent"
        The "/" separates petitioner's advocate from respondent's advocate.
        """
        # Find all lines that contain "/" which typically indicates advocate separator
        adv_petitioner = ""
        adv_respondent = ""

        # Look for the pattern after V/s and respondent name
        vs_pattern = re.compile(r"\bV/s\b", re.IGNORECASE)
        vs_match = vs_pattern.search(text)

        if not vs_match:
            return ("", "")

        # Advocates are typically after the respondent line
        after_vs = text[vs_match.end():]
        lines = after_vs.split("\n")

        # Find lines containing "/" which separates pet/res advocates
        advocate_parts = []
        for line in lines:
            line = line.strip()
            if "/" in line and "V/s" not in line:
                advocate_parts.append(line)

        if advocate_parts:
            # Join all advocate lines and split by "/"
            full_adv_text = " ".join(advocate_parts)
            # Split by the first "/" that's not part of case number
            parts = full_adv_text.split("/", 1)
            if len(parts) == 2:
                adv_petitioner = parts[0].strip()
                adv_respondent = parts[1].strip()
                # Clean up — remove "None" or empty
                if adv_respondent.lower() in ["none", "none for r-1 to 3"]:
                    adv_respondent = "None"
            elif len(parts) == 1:
                adv_petitioner = parts[0].strip()

        # Remove respondent name that might have leaked into advocate field
        for noise in ["UOI & Ors", "UOI & Ors.", "UOi & Ors."]:
            adv_petitioner = adv_petitioner.replace(noise, "").strip()
            adv_respondent = adv_respondent.replace(noise, "").strip()

        return (adv_petitioner[:200], adv_respondent[:200])

    def _detect_category(self, text: str) -> str:
        """Detect the case category from surrounding text."""
        categories = [
            ("ADMISSION MATTERS", "admission"),
            ("MA (EXECUTION)", "execution"),
            ("MA (OTHERS)", "ma_others"),
            ("RAs", "review"),
            ("Pleadings Not Complete", "pleadings_incomplete"),
            ("FOR FINAL HEARING", "final_hearing"),
            ("PART HEARD", "part_heard"),
            ("BY COURT", "court_order"),
            ("REGULAR LIST", "regular"),
        ]
        # This is approximate — category headers appear before case entries
        # In practice, we'd track the last seen category header
        for pattern, category in categories:
            if pattern.lower() in text.lower():
                return category
        return "unknown"

    def _split_parties(self, text: str) -> tuple:
        """Split 'Petitioner vs Respondent' text."""
        if not text:
            return ("", "")
        for sep in [" V/s ", " vs ", " v/s ", " versus ", " Vs ", " V/S ", " VS "]:
            if sep in text:
                parts = text.split(sep, 1)
                return (parts[0].strip(), parts[1].strip())
        return (text.strip(), "")
