"""Rate limiter service for the Nyaya Sutra Backend API.

Implements tier-based daily search rate limiting using an in-memory
dictionary. Keys are formatted as '{user_id}:{date_ist}' so counters
naturally reset at midnight IST (UTC+5:30).

Note: For multi-instance deployment, replace the in-memory dict with
Redis using the REDIS_URL from app config.
"""

import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

# IST timezone offset: UTC+5:30
IST = timezone(timedelta(hours=5, minutes=30))


class RateLimiter:
    """Tier-based daily rate limiter for search operations."""

    TIER_LIMITS = {
        "free": 10,
        "individual": 50,
        "advocate_normal": 200,
        "advocate_premium": None,  # Unlimited
    }

    def __init__(self):
        """Initialize with in-memory storage.

        Storage format: {'{user_id}:{date_ist}': count}
        The date_ist key component ensures natural daily reset at midnight IST.
        """
        # In-memory storage for single-instance deployment.
        # For multi-instance, use Redis with REDIS_URL from config.
        self._counts: dict[str, int] = {}

    def _get_key(self, user_id: str) -> str:
        """Generate the storage key for a user's daily counter.

        Uses the current IST date so the counter resets at midnight IST.

        Args:
            user_id: The user's identifier.

        Returns:
            Key string in format '{user_id}:{YYYY-MM-DD}'.
        """
        now_ist = datetime.now(IST)
        date_str = now_ist.strftime("%Y-%m-%d")
        return f"{user_id}:{date_str}"

    def _get_count(self, user_id: str) -> int:
        """Get the current daily search count for a user.

        Args:
            user_id: The user's identifier.

        Returns:
            Current count for today (0 if no searches yet).
        """
        key = self._get_key(user_id)
        return self._counts.get(key, 0)

    def check_limit(self, user_id: str, tier: str) -> dict:
        """Check if a user is within their daily search limit.

        Args:
            user_id: The user's identifier.
            tier: The user's subscription tier.

        Returns:
            Dict with:
                - allowed (bool): Whether the user can perform a search.
                - remaining (int or None): Remaining searches (None if unlimited).
                - limit (int or None): Daily limit for the tier (None if unlimited).
                - reset_at (str): ISO timestamp of next midnight IST.
        """
        limit = self.TIER_LIMITS.get(tier)

        # Unlimited tier
        if limit is None:
            return {
                "allowed": True,
                "remaining": None,
                "limit": None,
                "reset_at": self.get_reset_time().isoformat(),
            }

        current_count = self._get_count(user_id)
        remaining = max(limit - current_count, 0)
        allowed = current_count < limit

        return {
            "allowed": allowed,
            "remaining": remaining,
            "limit": limit,
            "reset_at": self.get_reset_time().isoformat(),
        }

    def increment(self, user_id: str) -> None:
        """Increment the user's daily search count.

        Args:
            user_id: The user's identifier.
        """
        key = self._get_key(user_id)
        self._counts[key] = self._counts.get(key, 0) + 1

    def get_reset_time(self) -> datetime:
        """Calculate the next midnight IST (UTC+5:30).

        Returns:
            Datetime of next midnight IST in UTC representation.
        """
        now_ist = datetime.now(IST)
        # Next midnight IST = today's date + 1 day at 00:00:00 IST
        tomorrow_ist = now_ist.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timedelta(days=1)
        return tomorrow_ist

    def get_remaining(self, user_id: str, tier: str) -> int:
        """Return remaining searches for today.

        Args:
            user_id: The user's identifier.
            tier: The user's subscription tier.

        Returns:
            Remaining search count. Returns -1 for unlimited tiers.
        """
        limit = self.TIER_LIMITS.get(tier)

        if limit is None:
            return -1  # Unlimited

        current_count = self._get_count(user_id)
        return max(limit - current_count, 0)
