"""Authentication middleware for the Nyaya Sutra Backend.

Provides the @require_auth decorator that:
1. Extracts JWT from Authorization header
2. Verifies signature and expiry
3. Checks session is not revoked
4. Attaches user_id and tier to Flask g object
"""

import hashlib
from functools import wraps

from flask import g, request
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from ..extensions import db
from ..middleware.error_handler import AuthenticationError
from ..models.user import UserSession


def require_auth(f):
    """Decorator that enforces JWT authentication and session validity.

    Attaches g.user_id and g.user_tier for downstream use.
    Returns 401 for missing/invalid/expired tokens or revoked sessions.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        # Verify JWT is present and valid
        try:
            verify_jwt_in_request()
        except Exception as e:
            raise AuthenticationError(
                "Authentication required. Please provide a valid token."
            )

        # Extract claims
        claims = get_jwt()
        user_id = claims.get("user_id", get_jwt_identity())
        tier = claims.get("tier", "free")

        # Check session is not revoked
        # Get the token from the Authorization header to compute hash
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()

            session = UserSession.query.filter_by(token_hash=token_hash).first()
            if session and session.revoked_at is not None:
                raise AuthenticationError(
                    "Session has been revoked. Please login again."
                )

        # Attach user info to g for downstream use
        g.user_id = user_id
        g.user_tier = tier

        return f(*args, **kwargs)

    return decorated
