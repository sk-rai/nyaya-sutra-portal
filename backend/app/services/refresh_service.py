"""Refresh service for the Nyaya Sutra Backend API.

Handles background case refresh, stale cache purging, and identification
of cases needing refresh. Uses PostgreSQL database functions for purge
and refresh queries.
"""

import logging
import time

from flask import current_app
from sqlalchemy import text

from ..extensions import db

logger = logging.getLogger(__name__)


class RefreshService:
    """Service handling background case refresh and cache cleanup."""

    def refresh_tracked_cases(self, batch_size: int = 10, delay_sec: float = 2.0) -> dict:
        """Refresh tracked cases that are due for update.

        Calls get_cases_needing_refresh() to identify cases, then processes
        them in batches. Currently, scrapers are not yet available, so all
        cases are skipped with a log message.

        Args:
            batch_size: Number of cases to process per batch.
            delay_sec: Seconds to wait between batches.

        Returns:
            Dict with counts: {refreshed, failed, skipped}.
        """
        cases = self.get_cases_needing_refresh()

        refreshed = 0
        failed = 0
        skipped = 0

        if not cases:
            logger.info("No cases needing refresh.")
            return {"refreshed": 0, "failed": 0, "skipped": 0}

        logger.info(f"Found {len(cases)} cases needing refresh.")

        # Process in batches
        for i in range(0, len(cases), batch_size):
            batch = cases[i:i + batch_size]

            for case in batch:
                court_code = case.get("court_code", "unknown")
                case_number = case.get("case_number", "unknown")

                # TODO: Call scraper to re-fetch when scrapers are built
                logger.info(
                    f"Scraper not yet available for {court_code} "
                    f"(case: {case_number}). Skipping."
                )
                skipped += 1

            # Sleep between batches to avoid overwhelming court servers
            if i + batch_size < len(cases):
                time.sleep(delay_sec)

        result = {"refreshed": refreshed, "failed": failed, "skipped": skipped}
        logger.info(f"Refresh complete: {result}")
        return result

    def purge_stale_cache(self) -> dict:
        """Invoke the purge_stale_cache PostgreSQL function.

        Calls purge_stale_cache(48, 24) which removes:
        - Untracked cases older than 48 hours
        - Inactive cases not accessed in 24 hours
        - Expired OTP tokens
        - Expired/revoked user sessions

        Returns:
            Dict with counts: {deleted_cases, deleted_hearings,
                               deleted_otps, deleted_sessions}.
        """
        try:
            result = db.session.execute(
                text("SELECT * FROM purge_stale_cache(48, 24)")
            )
            row = result.fetchone()

            if row:
                counts = {
                    "deleted_cases": row[0] if row[0] is not None else 0,
                    "deleted_hearings": row[1] if row[1] is not None else 0,
                    "deleted_otps": row[2] if row[2] is not None else 0,
                    "deleted_sessions": row[3] if row[3] is not None else 0,
                }
            else:
                counts = {
                    "deleted_cases": 0,
                    "deleted_hearings": 0,
                    "deleted_otps": 0,
                    "deleted_sessions": 0,
                }

            db.session.commit()

            logger.info(f"Purge stale cache complete: {counts}")
            return counts

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error purging stale cache: {e}")
            return {
                "deleted_cases": 0,
                "deleted_hearings": 0,
                "deleted_otps": 0,
                "deleted_sessions": 0,
            }

    def get_cases_needing_refresh(self) -> list:
        """Call the get_cases_needing_refresh PostgreSQL function.

        Executes get_cases_needing_refresh(24, 12) which returns cases
        where tracked cases haven't been refreshed within their tier's
        refresh window (24h for normal tiers, 12h for premium).

        Returns:
            List of dicts with: case_id, court_code, case_number,
                                source_url, max_tier.
        """
        try:
            result = db.session.execute(
                text("SELECT * FROM get_cases_needing_refresh(24, 12)")
            )
            rows = result.fetchall()

            cases = []
            for row in rows:
                cases.append({
                    "case_id": str(row[0]) if row[0] else None,
                    "court_code": row[1] if len(row) > 1 else None,
                    "case_number": row[2] if len(row) > 2 else None,
                    "source_url": row[3] if len(row) > 3 else None,
                    "max_tier": row[4] if len(row) > 4 else None,
                })

            return cases

        except Exception as e:
            logger.error(f"Error getting cases needing refresh: {e}")
            return []
