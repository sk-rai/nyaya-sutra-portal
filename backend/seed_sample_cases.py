"""Seed sample case data for testing.

Populates case_cache and case_hearings with realistic data for:
- AFT Delhi (5 cases)
- AFT Mumbai (3 cases)
- CAT Delhi (4 cases)
- CAT Mumbai (3 cases)
- Delhi High Court (3 cases)
- Supreme Court (2 cases)

All cases have June 2026 hearing dates for testing.

Run: python seed_sample_cases.py
"""

import os
import sys
from datetime import date, datetime, timezone

# Fix Render's DATABASE_URL format
database_url = os.environ.get("DATABASE_URL", "")
if database_url.startswith("postgres://"):
    os.environ["DATABASE_URL"] = database_url.replace("postgres://", "postgresql://", 1)

from app import create_app
from app.extensions import db
from app.models.case import CaseCache, CaseHearing

SAMPLE_CASES = [
    # ─── AFT Delhi ──────────────────────────────────────────────────
    {
        "court_code": "aft_del",
        "case_number": "OA 234/2025",
        "case_title": "Ex Sub Maj Rajesh Kumar vs Union of India",
        "petitioner": "Ex Sub Maj Rajesh Kumar",
        "respondent": "Union of India through MOD",
        "advocate_petitioner": "Adv. S.K. Sharma",
        "advocate_respondent": "Adv. R.P. Singh (CGSC)",
        "bench": "Hon'ble Justice S.S. Rawat & Lt Gen P.M. Hariz",
        "item_number": "3",
        "case_type": "Original Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 10),
        "last_hearing_date": date(2026, 5, 8),
    },
    {
        "court_code": "aft_del",
        "case_number": "OA 567/2024",
        "case_title": "Col (Retd) Vikram Singh vs Chief of Army Staff",
        "petitioner": "Col (Retd) Vikram Singh",
        "respondent": "Chief of Army Staff & Ors",
        "advocate_petitioner": "Adv. Anil Katiyar",
        "advocate_respondent": "Adv. M.K. Gupta (CGSC)",
        "bench": "Hon'ble Justice S.S. Rawat & Lt Gen P.M. Hariz",
        "item_number": "7",
        "case_type": "Original Application",
        "case_status": "part_heard",
        "next_hearing_date": date(2026, 6, 12),
        "last_hearing_date": date(2026, 5, 15),
    },
    {
        "court_code": "aft_del",
        "case_number": "TA 89/2026",
        "case_title": "Nb Sub Mohan Lal vs Union of India",
        "petitioner": "Nb Sub Mohan Lal",
        "respondent": "Union of India through MOD",
        "advocate_petitioner": "Adv. Priya Verma",
        "advocate_respondent": "Adv. R.P. Singh (CGSC)",
        "bench": "Hon'ble Justice S.S. Rawat & Air Marshal B.K. Pandey",
        "item_number": "12",
        "case_type": "Transfer Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 17),
        "last_hearing_date": date(2026, 4, 22),
    },
    {
        "court_code": "aft_del",
        "case_number": "MA 45/2026",
        "case_title": "Wg Cdr (Retd) Amit Sharma vs Union of India",
        "petitioner": "Wg Cdr (Retd) Amit Sharma",
        "respondent": "Union of India through MOD & CAS",
        "advocate_petitioner": "Adv. D.K. Thakur",
        "advocate_respondent": "Adv. S. Banerjee (CGSC)",
        "bench": "Hon'ble Justice S.S. Rawat & Air Marshal B.K. Pandey",
        "item_number": "5",
        "case_type": "Miscellaneous Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 19),
        "last_hearing_date": date(2026, 5, 20),
    },
    {
        "court_code": "aft_del",
        "case_number": "OA 890/2025",
        "case_title": "Hav Suresh Yadav vs Union of India",
        "petitioner": "Hav Suresh Yadav",
        "respondent": "Union of India through MOD",
        "advocate_petitioner": "Adv. Neha Gupta",
        "advocate_respondent": "Adv. R.P. Singh (CGSC)",
        "bench": "Hon'ble Justice S.S. Rawat & Lt Gen P.M. Hariz",
        "item_number": "15",
        "case_type": "Original Application",
        "case_status": "reserved",
        "next_hearing_date": date(2026, 6, 24),
        "last_hearing_date": date(2026, 5, 27),
    },
    # ─── AFT Mumbai ─────────────────────────────────────────────────
    {
        "court_code": "aft_mum",
        "case_number": "OA 112/2025",
        "case_title": "Ex Sgt Ramesh Patil vs Union of India",
        "petitioner": "Ex Sgt Ramesh Patil",
        "respondent": "Union of India through MOD",
        "advocate_petitioner": "Adv. V.R. Deshmukh",
        "advocate_respondent": "Adv. A.S. Kulkarni (CGSC)",
        "bench": "Hon'ble Justice R.K. Gauba & Vice Admiral S.N. Ghormade",
        "item_number": "2",
        "case_type": "Original Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 5),
        "last_hearing_date": date(2026, 5, 6),
    },
    {
        "court_code": "aft_mum",
        "case_number": "OA 345/2026",
        "case_title": "Cdr (Retd) Anil Joshi vs Chief of Naval Staff",
        "petitioner": "Cdr (Retd) Anil Joshi",
        "respondent": "Chief of Naval Staff & Ors",
        "advocate_petitioner": "Adv. P.K. Mhatre",
        "advocate_respondent": "Adv. S.M. Jadhav (CGSC)",
        "bench": "Hon'ble Justice R.K. Gauba & Vice Admiral S.N. Ghormade",
        "item_number": "8",
        "case_type": "Original Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 11),
        "last_hearing_date": date(2026, 5, 13),
    },
    {
        "court_code": "aft_mum",
        "case_number": "TA 23/2026",
        "case_title": "Sep Dinesh More vs Union of India",
        "petitioner": "Sep Dinesh More",
        "respondent": "Union of India through MOD",
        "advocate_petitioner": "Adv. R.S. Shinde",
        "advocate_respondent": "Adv. A.S. Kulkarni (CGSC)",
        "bench": "Hon'ble Justice R.K. Gauba & Vice Admiral S.N. Ghormade",
        "item_number": "11",
        "case_type": "Transfer Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 18),
        "last_hearing_date": date(2026, 5, 19),
    },
    # ─── CAT Delhi ──────────────────────────────────────────────────
    {
        "court_code": "cat_del",
        "case_number": "OA 1234/2025",
        "case_title": "Sh. Arvind Mishra vs Union of India",
        "petitioner": "Sh. Arvind Mishra (Under Secretary, MoF)",
        "respondent": "Union of India through DoPT",
        "advocate_petitioner": "Adv. K.L. Mehta",
        "advocate_respondent": "Adv. N. Sharma (CGSC)",
        "bench": "Hon'ble Chairman Justice R.K. Srivastava & Member (A) Sh. B.P. Sharma",
        "item_number": "4",
        "case_type": "Original Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 3),
        "last_hearing_date": date(2026, 5, 5),
    },
    {
        "court_code": "cat_del",
        "case_number": "OA 2567/2024",
        "case_title": "Smt. Sunita Devi vs UPSC",
        "petitioner": "Smt. Sunita Devi",
        "respondent": "Union Public Service Commission & Ors",
        "advocate_petitioner": "Adv. R.K. Anand",
        "advocate_respondent": "Adv. P.K. Jain (CGSC)",
        "bench": "Hon'ble Chairman Justice R.K. Srivastava & Member (A) Sh. B.P. Sharma",
        "item_number": "9",
        "case_type": "Original Application",
        "case_status": "part_heard",
        "next_hearing_date": date(2026, 6, 9),
        "last_hearing_date": date(2026, 5, 12),
    },
    {
        "court_code": "cat_del",
        "case_number": "OA 789/2026",
        "case_title": "Sh. Manoj Kumar vs Ministry of Railways",
        "petitioner": "Sh. Manoj Kumar (Sr. Section Engineer)",
        "respondent": "Union of India through Ministry of Railways",
        "advocate_petitioner": "Adv. S.S. Hooda",
        "advocate_respondent": "Adv. V.K. Bansal (CGSC)",
        "bench": "Hon'ble Justice A.K. Bishnoi & Member (A) Sh. R.P. Meena",
        "item_number": "6",
        "case_type": "Original Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 16),
        "last_hearing_date": date(2026, 5, 18),
    },
    {
        "court_code": "cat_del",
        "case_number": "MA 456/2026",
        "case_title": "Sh. Ravi Shankar vs DoPT",
        "petitioner": "Sh. Ravi Shankar (Section Officer)",
        "respondent": "Union of India through DoPT",
        "advocate_petitioner": "Adv. A.K. Tyagi",
        "advocate_respondent": "Adv. N. Sharma (CGSC)",
        "bench": "Hon'ble Justice A.K. Bishnoi & Member (A) Sh. R.P. Meena",
        "item_number": "14",
        "case_type": "Miscellaneous Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 23),
        "last_hearing_date": date(2026, 5, 25),
    },
    # ─── CAT Mumbai ─────────────────────────────────────────────────
    {
        "court_code": "cat_mum",
        "case_number": "OA 678/2025",
        "case_title": "Sh. Prakash Jadhav vs Western Railway",
        "petitioner": "Sh. Prakash Jadhav (Loco Pilot)",
        "respondent": "Union of India through GM, Western Railway",
        "advocate_petitioner": "Adv. M.S. Patil",
        "advocate_respondent": "Adv. R.K. Deshpande (CGSC)",
        "bench": "Hon'ble Justice M.B. Gosavi & Member (A) Sh. S.K. Mishra",
        "item_number": "1",
        "case_type": "Original Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 4),
        "last_hearing_date": date(2026, 5, 7),
    },
    {
        "court_code": "cat_mum",
        "case_number": "OA 901/2026",
        "case_title": "Smt. Kavita Sawant vs CGDA",
        "petitioner": "Smt. Kavita Sawant (Accounts Officer)",
        "respondent": "Controller General of Defence Accounts",
        "advocate_petitioner": "Adv. N.V. Khandekar",
        "advocate_respondent": "Adv. S.P. Raut (CGSC)",
        "bench": "Hon'ble Justice M.B. Gosavi & Member (A) Sh. S.K. Mishra",
        "item_number": "10",
        "case_type": "Original Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 13),
        "last_hearing_date": date(2026, 5, 14),
    },
    {
        "court_code": "cat_mum",
        "case_number": "TA 67/2026",
        "case_title": "Sh. Vijay Bhosale vs Customs Dept",
        "petitioner": "Sh. Vijay Bhosale (Inspector, Customs)",
        "respondent": "Union of India through CBIC",
        "advocate_petitioner": "Adv. A.R. Mane",
        "advocate_respondent": "Adv. R.K. Deshpande (CGSC)",
        "bench": "Hon'ble Justice M.B. Gosavi & Member (A) Sh. S.K. Mishra",
        "item_number": "13",
        "case_type": "Transfer Application",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 20),
        "last_hearing_date": date(2026, 5, 21),
    },
    # ─── Delhi High Court ───────────────────────────────────────────
    {
        "court_code": "hc_del",
        "case_number": "WP(C) 4567/2025",
        "case_title": "Ex Maj Gen A.K. Singh vs Union of India",
        "petitioner": "Ex Maj Gen A.K. Singh",
        "respondent": "Union of India & Ors",
        "advocate_petitioner": "Sr. Adv. Harish Salve with Adv. R. Balasubramanian",
        "advocate_respondent": "ASG Tushar Mehta",
        "bench": "Hon'ble Justice Rajiv Shakdher & Justice Girish Kathpalia",
        "item_number": "21",
        "case_type": "Writ Petition (Civil)",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 6),
        "last_hearing_date": date(2026, 5, 9),
    },
    {
        "court_code": "hc_del",
        "case_number": "WP(C) 8901/2024",
        "case_title": "All India Defence Employees Federation vs Union of India",
        "petitioner": "All India Defence Employees Federation",
        "respondent": "Union of India through MOD",
        "advocate_petitioner": "Sr. Adv. Colin Gonsalves with Adv. S. Muralidhar",
        "advocate_respondent": "Adv. Anil Soni (CGSC)",
        "bench": "Hon'ble Chief Justice Manmohan & Justice Tushar Rao Gedela",
        "item_number": "35",
        "case_type": "Writ Petition (Civil)",
        "case_status": "part_heard",
        "next_hearing_date": date(2026, 6, 15),
        "last_hearing_date": date(2026, 5, 16),
    },
    {
        "court_code": "hc_del",
        "case_number": "LPA 234/2026",
        "case_title": "Union of India vs Ex Col Deepak Rao",
        "petitioner": "Union of India through MOD",
        "respondent": "Ex Col Deepak Rao",
        "advocate_petitioner": "Adv. Rajesh Gogna (CGSC)",
        "advocate_respondent": "Adv. P.S. Narasimha",
        "bench": "Hon'ble Justice Vibhu Bakhru & Justice Amit Mahajan",
        "item_number": "18",
        "case_type": "Letters Patent Appeal",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 25),
        "last_hearing_date": date(2026, 5, 28),
    },
    # ─── Supreme Court ──────────────────────────────────────────────
    {
        "court_code": "sc",
        "case_number": "SLP(C) 12345/2025",
        "case_title": "Union of India vs Ex Lt Gen P.K. Sehgal",
        "petitioner": "Union of India through MOD",
        "respondent": "Ex Lt Gen P.K. Sehgal",
        "advocate_petitioner": "Solicitor General Tushar Mehta",
        "advocate_respondent": "Sr. Adv. Fali Nariman with Adv. A.K. Panda",
        "bench": "Hon'ble CJI D.Y. Chandrachud & Justice J.B. Pardiwala & Justice Manoj Misra",
        "item_number": "501",
        "case_type": "Special Leave Petition (Civil)",
        "case_status": "pending",
        "next_hearing_date": date(2026, 6, 2),
        "last_hearing_date": date(2026, 5, 2),
    },
    {
        "court_code": "sc",
        "case_number": "CA 7890/2024",
        "case_title": "Ex Brig Harinder Singh vs Chief of Army Staff",
        "petitioner": "Ex Brig Harinder Singh",
        "respondent": "Chief of Army Staff & Union of India",
        "advocate_petitioner": "Sr. Adv. K.K. Venugopal with Adv. Meenakshi Arora",
        "advocate_respondent": "AG R. Venkataramani",
        "bench": "Hon'ble Justice Sanjiv Khanna & Justice B.R. Gavai",
        "item_number": "302",
        "case_type": "Civil Appeal",
        "case_status": "part_heard",
        "next_hearing_date": date(2026, 6, 26),
        "last_hearing_date": date(2026, 5, 22),
    },
]


def seed_cases():
    """Insert sample cases into the database."""
    app = create_app(os.getenv("FLASK_ENV", "production"))

    with app.app_context():
        created = 0
        skipped = 0

        for case_data in SAMPLE_CASES:
            # Check if already exists
            existing = CaseCache.query.filter_by(
                court_code=case_data["court_code"],
                case_number=case_data["case_number"],
            ).first()

            if existing:
                print(f"  Skipped (exists): {case_data['court_code']}/{case_data['case_number']}")
                skipped += 1
                continue

            case = CaseCache(
                court_code=case_data["court_code"],
                case_number=case_data["case_number"],
                case_title=case_data["case_title"],
                petitioner=case_data["petitioner"],
                respondent=case_data["respondent"],
                advocate_petitioner=case_data["advocate_petitioner"],
                advocate_respondent=case_data.get("advocate_respondent", ""),
                bench=case_data["bench"],
                item_number=case_data["item_number"],
                case_type=case_data["case_type"],
                case_status=case_data["case_status"],
                next_hearing_date=case_data["next_hearing_date"],
                last_hearing_date=case_data.get("last_hearing_date"),
                parse_confidence=0.95,
                source_url=f"https://example.com/{case_data['court_code']}/cause-list",
                scraper_version="1.0.0",
                fetched_at=datetime.now(timezone.utc),
                raw_scraped_data={
                    "source": "seed_script",
                    "case_number": case_data["case_number"],
                    "parties": case_data["case_title"],
                },
            )
            db.session.add(case)
            db.session.flush()

            # Add a hearing record for last hearing
            if case_data.get("last_hearing_date"):
                hearing = CaseHearing(
                    case_id=case.id,
                    hearing_date=case_data["last_hearing_date"],
                    bench=case_data["bench"],
                    item_number=case_data["item_number"],
                    order_summary="Matter heard. Next date fixed.",
                )
                db.session.add(hearing)

            created += 1
            print(f"  Created: {case_data['court_code']}/{case_data['case_number']} (next: {case_data['next_hearing_date']})")

        db.session.commit()
        print(f"\nDone: {created} cases created, {skipped} skipped.")
        print(f"Total cases in DB: {CaseCache.query.count()}")


if __name__ == "__main__":
    print("Seeding sample case data (June 2026 cause lists)...\n")
    seed_cases()
