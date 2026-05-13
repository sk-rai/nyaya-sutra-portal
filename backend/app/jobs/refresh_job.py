"""Background job: Refresh tracked cases.

Wraps RefreshService.refresh_tracked_cases() with logging and error handling.
Processes in batches of 10 with 2-second delay between requests.
"""

import logging
import time

logger = logging.getLogger(__name__)

# Configuration
BATCH_SIZE = 10
DELAY_SECONDS = 2


def run_refresh_tracked_cases():
    """Execute the tracked case refresh job.

    Fetches cases needing refresh, scrapes them in batches,
    and logs the results (refreshed, failed, skipped counts).
    """
    from ..services.refresh_service import RefreshService

    logger.info("Starting refresh_tracked_cases job...")
    start_time = time.time()

    try:
        service = RefreshService()
        result = service.refresh_tracked_cases(
            batch_size=BATCH_SIZE,
            delay_sec=DELAY_SECONDS,
        )

        elapsed = time.time() - start_time
        logger.info(
            f"Refresh job complete in {elapsed:.1f}s — "
            f"refreshed={result.get('refreshed', 0)}, "
            f"failed={result.get('failed', 0)}, "
            f"skipped={result.get('skipped', 0)}"
        )

    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(
            f"Refresh job failed after {elapsed:.1f}s: {e}",
            exc_info=True,
        )
