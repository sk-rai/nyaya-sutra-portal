"""Rate limiting middleware for the Nyaya Sutra Backend.

Provides the @rate_limited decorator that:
1. Reads tier from g.user_tier (set by auth middleware or JWT)
2. Checks daily search count against tier limits
3. Returns 429 with reset time when limit exceeded
4. Increments counter on success
"""

from functools import wraps

from flask import g
from flask_jwt_extended import get_jwt, get_jwt_identity

from ..middleware.error_handler import RateLimitError
from ..services.rate_limiter import RateLimiter


def rate_limited(f):
    """Decorator that enforces tier-based rate limiting.

    Requires that the user is authenticated (g.user_id and g.user_tier set).
    Returns 429 with reset_time when the daily limit is exceeded.
    Increments the counter after successful execution.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        # Get user info - prefer g attributes, fall back to JWT claims
        user_id = getattr(g, "user_id", None)
        tier = getattr(g, "user_tier", None)

        if not user_id:
            claims = get_jwt()
            user_id = claims.get("user_id", get_jwt_identity())
            tier = claims.get("tier", "free")

        # Check rate limit
        limiter = RateLimiter()
        limiter.check_limit(user_id, tier)

        # Execute the wrapped function
        result = f(*args, **kwargs)

        # Increment counter after successful execution
        limiter.increment(user_id)

        return result

    return decorated
