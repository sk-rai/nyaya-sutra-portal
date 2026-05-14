"""Seed test accounts for all tiers.

Creates test users that can be used for testing across all subscription tiers.
These accounts have a fixed OTP bypass (code: 111111) for easy testing.

Run this script once after deployment:
    python seed_test_accounts.py

Test accounts created:
    - admin@nyayasutra.test / 9900000001 — advocate_premium + admin flag
    - premium@nyayasutra.test / 9900000002 — advocate_premium
    - advocate@nyayasutra.test / 9900000003 — advocate_normal
    - individual@nyayasutra.test / 9900000004 — individual (paid)
    - free@nyayasutra.test / 9900000005 — free tier
"""

import os
import sys

# Fix Render's DATABASE_URL format
database_url = os.environ.get("DATABASE_URL", "")
if database_url.startswith("postgres://"):
    os.environ["DATABASE_URL"] = database_url.replace("postgres://", "postgresql://", 1)

from app import create_app
from app.extensions import db
from app.models.user import User

TEST_ACCOUNTS = [
    {
        "name": "Admin Test User",
        "email": "admin@nyayasutra.test",
        "phone": "9900000001",
        "user_type": "advocate",
        "tier": "advocate_premium",
        "is_verified": True,
        "is_admin": True,
        "enrollment_no": "TEST/ADMIN/2024",
        "bar_council": "Delhi",
    },
    {
        "name": "Premium Advocate",
        "email": "premium@nyayasutra.test",
        "phone": "9900000002",
        "user_type": "advocate",
        "tier": "advocate_premium",
        "is_verified": True,
        "enrollment_no": "TEST/PREM/2024",
        "bar_council": "Delhi",
    },
    {
        "name": "Normal Advocate",
        "email": "advocate@nyayasutra.test",
        "phone": "9900000003",
        "user_type": "advocate",
        "tier": "advocate_normal",
        "is_verified": True,
        "enrollment_no": "TEST/ADV/2024",
        "bar_council": "Mumbai",
    },
    {
        "name": "Individual User",
        "email": "individual@nyayasutra.test",
        "phone": "9900000004",
        "user_type": "individual",
        "tier": "individual",
        "is_verified": True,
    },
    {
        "name": "Free User",
        "email": "free@nyayasutra.test",
        "phone": "9900000005",
        "user_type": "individual",
        "tier": "free",
        "is_verified": True,
    },
]


def seed_accounts():
    """Create test accounts if they don't already exist."""
    app = create_app(os.getenv("FLASK_ENV", "production"))

    with app.app_context():
        created = 0
        skipped = 0

        for account in TEST_ACCOUNTS:
            # Check if already exists
            existing = User.query.filter(
                (User.email == account["email"]) | (User.phone == account["phone"])
            ).first()

            if existing:
                # Update tier if needed
                if existing.tier != account["tier"]:
                    existing.tier = account["tier"]
                    existing.is_verified = True
                    db.session.commit()
                    print(f"  Updated: {account['email']} -> tier={account['tier']}")
                else:
                    print(f"  Skipped (exists): {account['email']} ({account['tier']})")
                skipped += 1
                continue

            user = User(
                name=account["name"],
                email=account["email"],
                phone=account["phone"],
                user_type=account["user_type"],
                tier=account["tier"],
                is_verified=account.get("is_verified", True),
                enrollment_no=account.get("enrollment_no"),
                bar_council=account.get("bar_council"),
            )
            db.session.add(user)
            db.session.commit()
            print(f"  Created: {account['email']} ({account['tier']})")
            created += 1

        print(f"\nDone: {created} created, {skipped} skipped.")
        print("\n--- Test Account Credentials ---")
        print("All accounts use OTP login. Check Render logs for OTP codes.")
        print("Or use the test OTP bypass (code: 111111) if enabled.\n")
        for acc in TEST_ACCOUNTS:
            admin_flag = " [ADMIN]" if acc.get("is_admin") else ""
            print(f"  {acc['tier']:20s} | {acc['email']:30s} | {acc['phone']}{admin_flag}")


if __name__ == "__main__":
    print("Seeding test accounts...")
    seed_accounts()
