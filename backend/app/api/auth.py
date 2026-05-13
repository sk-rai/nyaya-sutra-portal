"""Auth API blueprint for the Nyaya Sutra Backend.

Endpoints:
- POST /api/auth/otp/request — Request OTP for login/register
- POST /api/auth/otp/verify — Verify OTP and get JWT
- POST /api/auth/register — Register a new user
- POST /api/auth/logout — Revoke current session
"""

from flask import Blueprint, request

from ..middleware.error_handler import ValidationError
from ..services.auth_service import AuthService
from ..utils.response import error_response, success_response

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/otp/request", methods=["POST"])
def request_otp():
    """Request an OTP for the given identifier (email or phone).

    Request body:
        {
            "identifier": "user@example.com" or "9876543210",
            "purpose": "login" (optional, default "login")
        }
    """
    data = request.get_json(silent=True)
    if not data:
        raise ValidationError("Request body must be valid JSON.")

    identifier = data.get("identifier", "").strip()
    purpose = data.get("purpose", "login")

    if not identifier:
        raise ValidationError("Identifier (email or phone) is required.")

    service = AuthService()
    result = service.request_otp(identifier, purpose)

    return success_response(result, status=200)


@auth_bp.route("/otp/verify", methods=["POST"])
def verify_otp():
    """Verify OTP and issue JWT token.

    Request body:
        {
            "identifier": "user@example.com" or "9876543210",
            "otp_code": "123456"
        }
    """
    data = request.get_json(silent=True)
    if not data:
        raise ValidationError("Request body must be valid JSON.")

    identifier = data.get("identifier", "").strip()
    otp_code = data.get("otp_code", "").strip()

    if not identifier:
        raise ValidationError("Identifier (email or phone) is required.")
    if not otp_code:
        raise ValidationError("OTP code is required.")

    service = AuthService()
    result = service.verify_otp(identifier, otp_code)

    return success_response(result, status=200)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user.

    Request body:
        {
            "email": "user@example.com" (optional if phone provided),
            "phone": "9876543210" (optional if email provided),
            "full_name": "John Doe",
            "user_type": "individual" | "advocate",
            "bar_council_id": "DEL/123/2020" (required for advocates),
            "specialization": "Criminal Law" (optional for advocates)
        }
    """
    data = request.get_json(silent=True)
    if not data:
        raise ValidationError("Request body must be valid JSON.")

    service = AuthService()
    result = service.register_user(data)

    return success_response(result, status=201)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Logout and revoke the current session.

    Requires Authorization header with Bearer token.

    Request body:
        {
            "session_id": "uuid-of-session"
        }
    """
    data = request.get_json(silent=True)
    if not data:
        raise ValidationError("Request body must be valid JSON.")

    session_id = data.get("session_id", "").strip()
    if not session_id:
        raise ValidationError("Session ID is required.")

    service = AuthService()
    service.logout(session_id)

    return success_response({"message": "Logged out successfully."}, status=200)
