"""APScheduler setup for the Nyaya Sutra Backend.

Configures interval-based background jobs:
- refresh_tracked_cases: every 6 hours
- purge_stale_cache: every 6 hours
- check_expiry: every 1 hour
"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

# Module-level scheduler instance
scheduler = BackgroundScheduler(daemon=True)


def init_scheduler(app):
    """Initialize and start the background scheduler.

    Registers all periodic jobs and starts the scheduler.
    Should be called once during app startup (not during testing).

    Args:
        app: The Flask application instance.
    """
    if scheduler.running:
        logger.info("Scheduler already running, skipping init.")
        return

    # Import job functions
    from .refresh_job import run_refresh_tracked_cases
    from .cleanup_job import run_cleanup

    # Wrap jobs with app context
    def refresh_with_context():
        with app.app_context():
            run_refresh_tracked_cases()

    def cleanup_with_context():
        with app.app_context():
            run_cleanup()

    def expiry_with_context():
        with app.app_context():
            from ..services.payment_service import PaymentService
            service = PaymentService()
            result = service.check_expiry()
            logger.info(f"Expiry check complete: {result}")

    # Register jobs
    scheduler.add_job(
        refresh_with_context,
        trigger=IntervalTrigger(hours=6),
        id="refresh_tracked_cases",
        name="Refresh tracked cases",
        replace_existing=True,
    )

    scheduler.add_job(
        cleanup_with_context,
        trigger=IntervalTrigger(hours=6),
        id="purge_stale_cache",
        name="Purge stale cache and expired records",
        replace_existing=True,
    )

    scheduler.add_job(
        expiry_with_context,
        trigger=IntervalTrigger(hours=1),
        id="check_subscription_expiry",
        name="Check and downgrade expired subscriptions",
        replace_existing=True,
    )

    # Start scheduler
    scheduler.start()
    logger.info("Background scheduler started with 3 jobs.")


def shutdown_scheduler():
    """Gracefully shut down the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Background scheduler shut down.")
