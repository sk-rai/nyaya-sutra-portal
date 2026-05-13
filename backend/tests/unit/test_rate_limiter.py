"""Unit tests for RateLimiter service."""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from app.services.rate_limiter import IST, RateLimiter


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def limiter():
    """Fresh RateLimiter instance."""
    return RateLimiter()


# ---------------------------------------------------------------------------
# check_limit Tests
# ---------------------------------------------------------------------------


class TestCheckLimit:
    """Tests for RateLimiter.check_limit."""

    def test_check_limit_within_limit(self, limiter):
        """User within limit should be allowed."""
        result = limiter.check_limit("user-1", "free")

        assert result["allowed"] is True
        assert result["remaining"] == 10
        assert result["limit"] == 10
        assert "reset_at" in result

    def test_check_limit_exceeded(self, limiter):
        """User at limit should be denied."""
        # Exhaust the free tier limit (10 searches)
        for _ in range(10):
            limiter.increment("user-1")

        result = limiter.check_limit("user-1", "free")

        assert result["allowed"] is False
        assert result["remaining"] == 0
        assert result["limit"] == 10

    def test_check_limit_premium_unlimited(self, limiter):
        """Premium tier should always be allowed with None remaining/limit."""
        # Even after many increments
        for _ in range(1000):
            limiter.increment("user-premium")

        result = limiter.check_limit("user-premium", "advocate_premium")

        assert result["allowed"] is True
        assert result["remaining"] is None
        assert result["limit"] is None

    def test_check_limit_individual_tier(self, limiter):
        """Individual tier should have limit of 50."""
        result = limiter.check_limit("user-ind", "individual")

        assert result["allowed"] is True
        assert result["remaining"] == 50
        assert result["limit"] == 50

    def test_check_limit_advocate_normal_tier(self, limiter):
        """Advocate normal tier should have limit of 200."""
        result = limiter.check_limit("user-adv", "advocate_normal")

        assert result["allowed"] is True
        assert result["remaining"] == 200
        assert result["limit"] == 200


# ---------------------------------------------------------------------------
# increment Tests
# ---------------------------------------------------------------------------


class TestIncrement:
    """Tests for RateLimiter.increment."""

    def test_increment_increases_count(self, limiter):
        """Increment should increase the daily count."""
        assert limiter._get_count("user-1") == 0

        limiter.increment("user-1")
        assert limiter._get_count("user-1") == 1

        limiter.increment("user-1")
        assert limiter._get_count("user-1") == 2

    def test_increment_separate_users(self, limiter):
        """Different users should have separate counters."""
        limiter.increment("user-a")
        limiter.increment("user-a")
        limiter.increment("user-b")

        assert limiter._get_count("user-a") == 2
        assert limiter._get_count("user-b") == 1


# ---------------------------------------------------------------------------
# get_reset_time Tests
# ---------------------------------------------------------------------------


class TestGetResetTime:
    """Tests for RateLimiter.get_reset_time."""

    def test_reset_at_midnight_ist(self, limiter):
        """Reset time should be next midnight IST."""
        reset_time = limiter.get_reset_time()

        # Should be in IST timezone
        assert reset_time.tzinfo == IST

        # Should be at midnight (00:00:00)
        assert reset_time.hour == 0
        assert reset_time.minute == 0
        assert reset_time.second == 0
        assert reset_time.microsecond == 0

        # Should be in the future
        now_ist = datetime.now(IST)
        assert reset_time > now_ist

    def test_reset_time_is_tomorrow(self, limiter):
        """Reset time should be tomorrow's midnight IST."""
        reset_time = limiter.get_reset_time()
        now_ist = datetime.now(IST)

        # Should be within 24 hours from now
        diff = reset_time - now_ist
        assert timedelta(0) < diff <= timedelta(hours=24)


# ---------------------------------------------------------------------------
# get_remaining Tests
# ---------------------------------------------------------------------------


class TestGetRemaining:
    """Tests for RateLimiter.get_remaining."""

    def test_get_remaining_full(self, limiter):
        """Fresh user should have full remaining count."""
        remaining = limiter.get_remaining("user-new", "free")
        assert remaining == 10

    def test_get_remaining_after_searches(self, limiter):
        """Remaining should decrease after increments."""
        limiter.increment("user-1")
        limiter.increment("user-1")
        limiter.increment("user-1")

        remaining = limiter.get_remaining("user-1", "free")
        assert remaining == 7

    def test_get_remaining_unlimited(self, limiter):
        """Premium tier should return -1 (unlimited)."""
        remaining = limiter.get_remaining("user-prem", "advocate_premium")
        assert remaining == -1

    def test_get_remaining_never_negative(self, limiter):
        """Remaining should never go below 0."""
        for _ in range(15):
            limiter.increment("user-1")

        remaining = limiter.get_remaining("user-1", "free")
        assert remaining == 0


# ---------------------------------------------------------------------------
# Daily Reset (key-based) Tests
# ---------------------------------------------------------------------------


class TestDailyReset:
    """Tests for daily reset behavior via date-based keys."""

    def test_different_days_have_separate_counts(self, limiter):
        """Searches on different days should have separate counters."""
        # Simulate today's searches
        limiter.increment("user-1")
        limiter.increment("user-1")

        today_count = limiter._get_count("user-1")
        assert today_count == 2

        # Manually insert a key for "yesterday" to verify separation
        now_ist = datetime.now(IST)
        yesterday = now_ist - timedelta(days=1)
        yesterday_key = f"user-1:{yesterday.strftime('%Y-%m-%d')}"
        limiter._counts[yesterday_key] = 5

        # Today's count should still be 2
        assert limiter._get_count("user-1") == 2

        # Yesterday's key should have 5
        assert limiter._counts[yesterday_key] == 5
