"""Quick test to verify the AFT parser works with real cause list text."""

import sys
sys.path.insert(0, '.')

from app.scrapers.aft_generic import AftGenericScraper

# Sample text from the real AFT Delhi cause list (25-March-2026)
SAMPLE_TEXT = """1
ARMED FORCES TRIBUNAL, PRINCIPAL BENCH, NEW DELHI
LIST OF BUSINESS
Date: 25-03-2026
Timing: 10:30 AM to 01.00 PM
& 02.00 PM to 04.30 PM
COURT No. 1 (Ground Floor)
THIS BENCH WILL NOT ASSEMBLE TODAY
CORAM:
HON'BLE THE CHAIRPERSON
HON'BLE REAR ADMIRAL DHIREN VIG
S.
No. Case No. Parties Name Advocate for Petitioner / Respondents
ADMISSION MATTERS
1. OA 750/2026 No 15707752-L Ex Hav Manphool
Singh
 V/s
UOI & Ors.
Devendra Kumar /
Kuldeep Singh
2. OA 751/2026
with
MA 1022/2026
Ex Hav Shailendra Kumar Singh (No.
15691068-W)
 V/s
UOI & Ors.
Devendra Kumar /
Prashant Gautam
MA (EXECUTION)
3. MA 4086/2022
with
MA 1145/2024
in
OA 1906/2020
AVM Laxmi Narain Sharma AVSM
(Retd) (18338-L)
 V/s
UOI & Ors
Ajit Kakkar /
Anil Gautam Sr CGSC
FOR FINAL HEARING
90. OA 1020/2019 Sub Zala Popat Sinh Zenu Sinh (JC
731192 K)
 V/s
UOI & Ors.
Archana Ramesh /
None
"""


def test_parser():
    """Test the AFT parser with real cause list text."""
    scraper = AftGenericScraper()

    # Test the text parser
    results = scraper._parse_full_text(SAMPLE_TEXT)

    print(f"Parsed {len(results)} cases from sample text\n")

    for i, result in enumerate(results):
        s = result.structured
        print(f"--- Case {i+1} ---")
        print(f"  Case Number: {s.get('case_number', 'N/A')}")
        print(f"  Petitioner: {s.get('petitioner', 'N/A')}")
        print(f"  Respondent: {s.get('respondent', 'N/A')}")
        print(f"  Advocate Pet: {s.get('advocate_petitioner', 'N/A')}")
        print(f"  Advocate Res: {s.get('advocate_respondent', 'N/A')}")
        print(f"  Bench: {s.get('bench', 'N/A')}")
        print(f"  Item No: {s.get('item_number', 'N/A')}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Related: {s.get('related_cases', [])}")
        print()

    # Check specific cases
    case_numbers = [r.structured.get("case_number") for r in results]
    print(f"All case numbers found: {case_numbers}")

    assert "OA 750/2026" in case_numbers, "OA 750/2026 not found!"
    assert "OA 751/2026" in case_numbers, "OA 751/2026 not found!"
    assert "MA 4086/2022" in case_numbers, "MA 4086/2022 not found!"
    assert "OA 1020/2019" in case_numbers, "OA 1020/2019 not found!"

    # Check OA 750/2026 details
    oa750 = next(r for r in results if r.structured.get("case_number") == "OA 750/2026")
    assert "Manphool" in oa750.structured.get("petitioner", ""), f"Petitioner wrong: {oa750.structured.get('petitioner')}"
    assert "Devendra Kumar" in oa750.structured.get("advocate_petitioner", ""), f"Adv wrong: {oa750.structured.get('advocate_petitioner')}"

    print("\n✅ ALL ASSERTIONS PASSED!")


if __name__ == "__main__":
    test_parser()
