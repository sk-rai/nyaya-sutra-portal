"""Unit tests for the global error handler and custom exception classes."""

import json
import logging

import pytest
from flask import Flask

from app.middleware.error_handler import (
    AppError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    TierInsufficientError,
    ValidationError,
    register_error_handlers,
)


@pytest.fixture
def app():
    """Create a Flask app with error handlers registered."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    register_error_handlers(app)

    # Add test routes that raise various errors
    @app.route("/raise-validation")
    def raise_validation():
        raise ValidationError("Email format is invalid", details={"field": "email"})

    @app.route("/raise-auth")
    def raise_auth():
        raise AuthenticationError("Token expired")

    @app.route("/raise-tier")
    def raise_tier():
        raise TierInsufficientError("Synopsis requires advocate_premium tier")

    @app.route("/raise-not-found")
    def raise_not_found():
        raise NotFoundError("Case not found")

    @app.route("/raise-rate-limit")
    def raise_rate_limit():
        raise RateLimitError(
            "Daily search limit reached. Resets at 00:00 IST.",
            details={"limit": 10, "reset_at": "2026-03-15T18:30:00Z"},
        )

    @app.route("/raise-unexpected")
    def raise_unexpected():
        raise RuntimeError("Something broke internally")

    @app.route("/raise-zero-division")
    def raise_zero_division():
        return str(1 / 0)

    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


class TestCustomExceptionClasses:
    """Tests for custom exception class attributes."""

    def test_validation_error_defaults(self):
        err = ValidationError()
        assert err.status_code == 400
        assert err.error_code == "VALIDATION_ERROR"
        assert err.details is None

    def test_validation_error_custom_message(self):
        err = ValidationError("Custom message", details={"field": "name"})
        assert err.message == "Custom message"
        assert err.details == {"field": "name"}

    def test_authentication_error_defaults(self):
        err = AuthenticationError()
        assert err.status_code == 401
        assert err.error_code == "UNAUTHORIZED"

    def test_tier_insufficient_error_defaults(self):
        err = TierInsufficientError()
        assert err.status_code == 403
        assert err.error_code == "TIER_INSUFFICIENT"

    def test_not_found_error_defaults(self):
        err = NotFoundError()
        assert err.status_code == 404
        assert err.error_code == "NOT_FOUND"

    def test_rate_limit_error_defaults(self):
        err = RateLimitError()
        assert err.status_code == 429
        assert err.error_code == "RATE_LIMIT_EXCEEDED"

    def test_app_error_base_defaults(self):
        err = AppError()
        assert err.status_code == 500
        assert err.error_code == "INTERNAL_ERROR"


class TestErrorHandlerResponses:
    """Tests for error handler HTTP responses."""

    def test_validation_error_returns_400(self, client):
        resp = client.get("/raise-validation")
        data = json.loads(resp.get_data(as_text=True))

        assert resp.status_code == 400
        assert data["success"] is False
        assert data["data"] is None
        assert data["error"]["code"] == "VALIDATION_ERROR"
        assert data["error"]["message"] == "Email format is invalid"
        assert data["error"]["details"] == {"field": "email"}

    def test_authentication_error_returns_401(self, client):
        resp = client.get("/raise-auth")
        data = json.loads(resp.get_data(as_text=True))

        assert resp.status_code == 401
        assert data["success"] is False
        assert data["error"]["code"] == "UNAUTHORIZED"
        assert data["error"]["message"] == "Token expired"

    def test_tier_insufficient_error_returns_403(self, client):
        resp = client.get("/raise-tier")
        data = json.loads(resp.get_data(as_text=True))

        assert resp.status_code == 403
        assert data["success"] is False
        assert data["error"]["code"] == "TIER_INSUFFICIENT"

    def test_not_found_error_returns_404(self, client):
        resp = client.get("/raise-not-found")
        data = json.loads(resp.get_data(as_text=True))

        assert resp.status_code == 404
        assert data["success"] is False
        assert data["error"]["code"] == "NOT_FOUND"

    def test_rate_limit_error_returns_429(self, client):
        resp = client.get("/raise-rate-limit")
        data = json.loads(resp.get_data(as_text=True))

        assert resp.status_code == 429
        assert data["success"] is False
        assert data["error"]["code"] == "RATE_LIMIT_EXCEEDED"
        assert data["error"]["details"]["limit"] == 10

    def test_unexpected_error_returns_500(self, client):
        resp = client.get("/raise-unexpected")
        data = json.loads(resp.get_data(as_text=True))

        assert resp.status_code == 500
        assert data["success"] is False
        assert data["error"]["code"] == "INTERNAL_ERROR"
        assert data["error"]["message"] == "An unexpected error occurred. Please try again later."

    def test_500_does_not_expose_internals(self, client):
        resp = client.get("/raise-unexpected")
        data = json.loads(resp.get_data(as_text=True))
        response_text = resp.get_data(as_text=True)

        # Must not contain internal error details
        assert "RuntimeError" not in response_text
        assert "Something broke internally" not in response_text
        assert "traceback" not in response_text.lower()

    def test_zero_division_returns_500(self, client):
        resp = client.get("/raise-zero-division")
        data = json.loads(resp.get_data(as_text=True))

        assert resp.status_code == 500
        assert data["error"]["code"] == "INTERNAL_ERROR"
        assert "ZeroDivisionError" not in resp.get_data(as_text=True)

    def test_nonexistent_route_returns_404(self, client):
        resp = client.get("/this-does-not-exist")
        data = json.loads(resp.get_data(as_text=True))

        assert resp.status_code == 404
        assert data["success"] is False
        assert data["error"]["code"] == "NOT_FOUND"

    def test_all_error_responses_have_envelope_format(self, client):
        """All error responses must have success, data, and error fields."""
        routes = [
            "/raise-validation",
            "/raise-auth",
            "/raise-tier",
            "/raise-not-found",
            "/raise-rate-limit",
            "/raise-unexpected",
        ]
        for route in routes:
            resp = client.get(route)
            data = json.loads(resp.get_data(as_text=True))
            assert "success" in data, f"Missing 'success' in {route}"
            assert "data" in data, f"Missing 'data' in {route}"
            assert "error" in data, f"Missing 'error' in {route}"
            assert data["success"] is False, f"'success' should be False in {route}"
            assert data["data"] is None, f"'data' should be None in {route}"

    def test_all_error_responses_are_json(self, client):
        """All error responses must have JSON content type."""
        routes = [
            "/raise-validation",
            "/raise-auth",
            "/raise-tier",
            "/raise-not-found",
            "/raise-rate-limit",
            "/raise-unexpected",
        ]
        for route in routes:
            resp = client.get(route)
            assert "application/json" in resp.content_type, f"Not JSON in {route}"


class TestServerSideLogging:
    """Tests that 500 errors log full traceback server-side."""

    def test_unexpected_error_logs_traceback(self, app, caplog):
        client = app.test_client()
        with caplog.at_level(logging.ERROR):
            client.get("/raise-unexpected")

        # Verify the error was logged server-side
        assert any("Unhandled exception" in record.message for record in caplog.records)
        # Verify exc_info was included (traceback logged)
        assert any(record.exc_info for record in caplog.records)
