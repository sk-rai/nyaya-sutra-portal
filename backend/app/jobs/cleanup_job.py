"""Background job: Cleanup stale cache and expired records.

Wraps RefreshService.purge_stale_cache() with logging and error handling.
Logs purge results (deleted_cases, deleted_hearings, deleted_otps, deleted_sessions).
"""

import logging
import time

logger = logging.getLogger(__name__)


def run_cleanup():
    """Execute the cleanup/purge job.

    Purges stale cached cases, expired OTP tokens, and expired sessions.
    Logs detailed results of what was cleaned up.
    """
    from ..services.refresh_service import RefreshService

    logger.info("Starting cleanup job...")
    start_time = time.time()

    try:
        service = RefreshService()
        result = service.purge_stale_cache()

        elapsed = time.time() - start_time
        logger.info(
            f"Cleanup job complete in {elapsed:.1f}s — "
            f"deleted_cases={result.get('deleted_cases', 0)}, "
            f"deleted_hearings={result.get('deleted_hearings', 0)}, "
            f"deleted_otps={result.get('deleted_otps', 0)}, "
            f"deleted_sessions={result.get('deleted_sessions', 0)}"
        )

    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(
            f"Cleanup job failed after {elapsed:.1f}s: {e}",
            exc_info=True,
        )
