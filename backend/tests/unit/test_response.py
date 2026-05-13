"""Unit tests for the standard response envelope utility."""

import json

import pytest
from flask import Flask

from app.utils.response import error_response, success_response


@pytest.fixture
def app():
    """Create a minimal Flask app for testing."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


class TestSuccessResponse:
    """Tests for success_response function."""

    def test_returns_correct_envelope_structure(self, app):
        with app.app_context():
            resp = success_response({"key": "value"})
            data = json.loads(resp.get_data(as_text=True))

            assert "success" in data
            assert "data" in data
            assert "error" in data

    def test_success_is_true(self, app):
        with app.app_context():
            resp = success_response({"items": [1, 2, 3]})
            data = json.loads(resp.get_data(as_text=True))

            assert data["success"] is True

    def test_data_contains_payload(self, app):
        with app.app_context():
            payload = {"name": "Test Case", "court": "AFT Delhi"}
            resp = success_response(payload)
            data = json.loads(resp.get_data(as_text=True))

            assert data["data"] == payload

    def test_error_is_null(self, app):
        with app.app_context():
            resp = success_response({"id": 1})
            data = json.loads(resp.get_data(as_text=True))

            assert data["error"] is None

    def test_default_status_is_200(self, app):
        with app.app_context():
            resp = success_response({"ok": True})

            assert resp.status_code == 200

    def test_custom_status_code(self, app):
        with app.app_context():
            resp = success_response({"id": 42}, status=201)

            assert resp.status_code == 201

    def test_content_type_is_json(self, app):
        with app.app_context():
            resp = success_response({})

            assert "application/json" in resp.content_type

    def test_data_can_be_list(self, app):
        with app.app_context():
            payload = [{"id": 1}, {"id": 2}]
            resp = success_response(payload)
            data = json.loads(resp.get_data(as_text=True))

            assert data["data"] == payload

    def test_data_can_be_none(self, app):
        with app.app_context():
            resp = success_response(None)
            data = json.loads(resp.get_data(as_text=True))

            assert data["data"] is None


class TestErrorResponse:
    """Tests for error_response function."""

    def test_returns_correct_envelope_structure(self, app):
        with app.app_context():
            resp = error_response("TEST_ERROR", "Something went wrong")
            data = json.loads(resp.get_data(as_text=True))

            assert "success" in data
            assert "data" in data
            assert "error" in data

    def test_success_is_false(self, app):
        with app.app_context():
            resp = error_response("TEST_ERROR", "Something went wrong")
            data = json.loads(resp.get_data(as_text=True))

            assert data["success"] is False

    def test_data_is_null(self, app):
        with app.app_context():
            resp = error_response("TEST_ERROR", "Something went wrong")
            data = json.loads(resp.get_data(as_text=True))

            assert data["data"] is None

    def test_error_contains_code_and_message(self, app):
        with app.app_context():
            resp = error_response("RATE_LIMIT_EXCEEDED", "Daily limit reached")
            data = json.loads(resp.get_data(as_text=True))

            assert data["error"]["code"] == "RATE_LIMIT_EXCEEDED"
            assert data["error"]["message"] == "Daily limit reached"

    def test_default_status_is_400(self, app):
        with app.app_context():
            resp = error_response("VALIDATION_ERROR", "Invalid input")

            assert resp.status_code == 400

    def test_custom_status_code(self, app):
        with app.app_context():
            resp = error_response("UNAUTHORIZED", "Missing token", status=401)

            assert resp.status_code == 401

    def test_details_included_when_provided(self, app):
        with app.app_context():
            details = {"limit": 10, "reset_at": "2026-03-15T18:30:00Z"}
            resp = error_response(
                "RATE_LIMIT_EXCEEDED",
                "Daily search limit reached.",
                details=details,
                status=429,
            )
            data = json.loads(resp.get_data(as_text=True))

            assert data["error"]["details"] == details

    def test_details_omitted_when_none(self, app):
        with app.app_context():
            resp = error_response("INTERNAL_ERROR", "Unexpected error", status=500)
            data = json.loads(resp.get_data(as_text=True))

            assert "details" not in data["error"]

    def test_content_type_is_json(self, app):
        with app.app_context():
            resp = error_response("TEST", "test")

            assert "application/json" in resp.content_type

    def test_500_error_response(self, app):
        with app.app_context():
            resp = error_response(
                "INTERNAL_ERROR",
                "An unexpected error occurred. Please try again later.",
                status=500,
            )
            data = json.loads(resp.get_data(as_text=True))

            assert resp.status_code == 500
            assert data["success"] is False
            assert data["data"] is None
            assert data["error"]["code"] == "INTERNAL_ERROR"
