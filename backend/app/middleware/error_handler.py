"""Global error handling for the Nyaya Sutra Backend API.

Provides custom exception classes and a registration function that installs
Flask error handlers for all standard HTTP error codes. All error responses
use the standard JSON envelope format.
"""

import traceback

from flask import current_app, jsonify
from werkzeug.exceptions import HTTPException

from ..utils.response import error_response


# ---------------------------------------------------------------------------
# Custom Exception Classes
# ---------------------------------------------------------------------------


class AppError(Exception):
    """Base application error with HTTP status and machine-readable code."""

    status_code = 500
    error_code = "INTERNAL_ERROR"
    message = "An unexpected error occurred."

    def __init__(self, message=None, details=None):
        super().__init__(message or self.message)
        if message:
            self.message = message
        self.details = details


class ValidationError(AppError):
    """Raised when request input fails validation (HTTP 400)."""

    status_code = 400
    error_code = "VALIDATION_ERROR"
    message = "Invalid input. Please check your request and try again."


class AuthenticationError(AppError):
    """Raised when authentication fails (HTTP 401)."""

    status_code = 401
    error_code = "UNAUTHORIZED"
    message = "Authentication required. Please provide a valid token."


class TierInsufficientError(AppError):
    """Raised when a feature requires a higher subscription tier (HTTP 403)."""

    status_code = 403
    error_code = "TIER_INSUFFICIENT"
    message = "This feature requires a higher subscription tier."


class NotFoundError(AppError):
    """Raised when a requested resource is not found (HTTP 404)."""

    status_code = 404
    error_code = "NOT_FOUND"
    message = "The requested resource was not found."


class RateLimitError(AppError):
    """Raised when the user exceeds their daily search quota (HTTP 429)."""

    status_code = 429
    error_code = "RATE_LIMIT_EXCEEDED"
    message = "Daily search limit reached. Please try again later."


# ---------------------------------------------------------------------------
# Error Handler Registration
# ---------------------------------------------------------------------------


def register_error_handlers(app):
    """Register global error handlers on the Flask application.

    Handles:
    - Custom AppError subclasses (ValidationError, AuthenticationError, etc.)
    - Standard Werkzeug HTTP exceptions (404, 405, etc.)
    - Unhandled exceptions (500 with server-side logging)

    Args:
        app: The Flask application instance.
    """

    @app.errorhandler(AppError)
    def handle_app_error(error):
        """Handle custom application errors."""
        return error_response(
            code=error.error_code,
            message=error.message,
            details=error.details,
            status=error.status_code,
        )

    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle 400 Bad Request."""
        message = "Bad request."
        if hasattr(error, "description") and error.description:
            message = error.description
        return error_response(
            code="VALIDATION_ERROR",
            message=message,
            status=400,
        )

    @app.errorhandler(401)
    def handle_unauthorized(error):
        """Handle 401 Unauthorized."""
        message = "Authentication required. Please provide a valid token."
        if hasattr(error, "description") and error.description:
            message = error.description
        return error_response(
            code="UNAUTHORIZED",
            message=message,
            status=401,
        )

    @app.errorhandler(403)
    def handle_forbidden(error):
        """Handle 403 Forbidden."""
        message = "You do not have permission to access this resource."
        if hasattr(error, "description") and error.description:
            message = error.description
        return error_response(
            code="TIER_INSUFFICIENT",
            message=message,
            status=403,
        )

    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 Not Found."""
        return error_response(
            code="NOT_FOUND",
            message="The requested resource was not found.",
            status=404,
        )

    @app.errorhandler(429)
    def handle_rate_limit(error):
        """Handle 429 Too Many Requests."""
        message = "Rate limit exceeded. Please try again later."
        if hasattr(error, "description") and error.description:
            message = error.description
        return error_response(
            code="RATE_LIMIT_EXCEEDED",
            message=message,
            status=429,
        )

    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 Internal Server Error.

        Logs the full traceback server-side but returns only a generic
        message to the client to avoid exposing internals.
        """
        current_app.logger.error(
            f"Unexpected error: {error}", exc_info=True
        )
        return error_response(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred. Please try again later.",
            status=500,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Catch-all handler for any unhandled exceptions.

        Logs the full traceback server-side but returns only a generic
        message to the client (never expose internals).
        """
        # If it's an HTTPException, let Werkzeug handle it with the
        # appropriate status code handler above
        if isinstance(error, HTTPException):
            return error.get_response()

        current_app.logger.error(
            f"Unhandled exception: {error}", exc_info=True
        )
        return error_response(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred. Please try again later.",
            status=500,
        )
