"""Subscriptions API blueprint for the Nyaya Sutra Backend.

Endpoints:
- POST /api/subscriptions/create-order — Create a Razorpay order for tier upgrade
- POST /api/subscriptions/webhook — Handle Razorpay payment webhooks
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from ..middleware.error_handler import ValidationError
from ..services.payment_service import PaymentService
from ..utils.response import success_response

subscriptions_bp = Blueprint("subscriptions", __name__, url_prefix="/api/subscriptions")


@subscriptions_bp.route("/create-order", methods=["POST"])
@jwt_required()
def create_order():
    """Create a Razorpay order for subscription upgrade.

    Request body:
        {
            "tier": "individual" | "advocate_normal" | "advocate_premium"
        }

    Requires JWT authentication.
    """
    data = request.get_json(silent=True)
    if not data:
        raise ValidationError("Request body must be valid JSON.")

    tier = data.get("tier", "").strip()
    if not tier:
        raise ValidationError("tier is required.")

    claims = get_jwt()
    user_id = claims.get("user_id", get_jwt_identity())

    service = PaymentService()
    result = service.create_order(user_id, tier)

    return success_response(result, status=201)


@subscriptions_bp.route("/webhook", methods=["POST"])
def handle_webhook():
    """Handle Razorpay payment webhook.

    No JWT required — uses Razorpay signature verification instead.
    """
    payload = request.get_json(silent=True)
    signature = request.headers.get("X-Razorpay-Signature", "")

    if not payload:
        raise ValidationError("Webhook payload must be valid JSON.")

    service = PaymentService()
    result = service.handle_webhook(payload, signature)

    return success_response(result)
