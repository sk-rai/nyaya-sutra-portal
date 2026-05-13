"""Payment service for the Nyaya Sutra Backend API.

Handles Razorpay order creation, payment verification, webhook processing,
and subscription expiry management. Supports a "mock mode" when Razorpay
credentials are not configured (for development/testing).
"""

import hashlib
import hmac
import logging
import time
from datetime import datetime, timedelta, timezone

from flask import current_app

from ..extensions import db
from ..middleware.error_handler import ValidationError
from ..models.subscription import Subscription
from ..models.user import User

logger = logging.getLogger(__name__)


class PaymentService:
    """Service handling Razorpay payment integration and subscription management."""

    TIER_AMOUNTS = {
        "individual": 5000,         # ₹50 in paise
        "advocate_normal": 19900,   # ₹199 in paise
        "advocate_premium": 59900,  # ₹599 in paise
    }

    def _is_mock_mode(self) -> bool:
        """Check if Razorpay keys are configured. If not, operate in mock mode."""
        key_id = current_app.config.get("RAZORPAY_KEY_ID", "")
        key_secret = current_app.config.get("RAZORPAY_KEY_SECRET", "")
        return not key_id or not key_secret

    def _get_razorpay_client(self):
        """Get a configured Razorpay client instance.

        Returns:
            razorpay.Client instance or None if in mock mode.
        """
        if self._is_mock_mode():
            return None

        import razorpay

        key_id = current_app.config["RAZORPAY_KEY_ID"]
        key_secret = current_app.config["RAZORPAY_KEY_SECRET"]
        return razorpay.Client(auth=(key_id, key_secret))

    def create_order(self, user_id: str, tier: str) -> dict:
        """Create a Razorpay order for the given tier.

        Args:
            user_id: The user's UUID string.
            tier: The subscription tier (individual, advocate_normal, advocate_premium).

        Returns:
            Dict with order_id, amount, currency, tier, and key_id.

        Raises:
            ValidationError: If tier is not valid.
        """
        if tier not in self.TIER_AMOUNTS:
            raise ValidationError(
                f"Invalid tier '{tier}'. Must be one of: {', '.join(self.TIER_AMOUNTS.keys())}"
            )

        amount = self.TIER_AMOUNTS[tier]
        receipt = f"nyaya_{user_id}_{tier}"

        if self._is_mock_mode():
            # Mock mode: return a fake order for development
            mock_order_id = f"order_mock_{int(time.time())}"
            logger.info(
                f"[MOCK] Created mock order {mock_order_id} for user {user_id}, "
                f"tier={tier}, amount={amount}"
            )
            return {
                "order_id": mock_order_id,
                "amount": amount,
                "currency": "INR",
                "tier": tier,
                "key_id": "rzp_test_mock",
            }

        # Real Razorpay mode
        client = self._get_razorpay_client()
        order_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": receipt,
            "notes": {
                "user_id": user_id,
                "tier": tier,
            },
        }

        order = client.order.create(data=order_data)

        return {
            "order_id": order["id"],
            "amount": amount,
            "currency": "INR",
            "tier": tier,
            "key_id": current_app.config["RAZORPAY_KEY_ID"],
        }

    def verify_payment(self, payment_data: dict) -> bool:
        """Verify Razorpay payment signature using HMAC-SHA256.

        Args:
            payment_data: Dict with razorpay_order_id, razorpay_payment_id,
                          and razorpay_signature.

        Returns:
            True if signature is valid, False otherwise.
        """
        if self._is_mock_mode():
            # Mock mode: always return True
            logger.info("[MOCK] Payment verification skipped (mock mode)")
            return True

        order_id = payment_data.get("razorpay_order_id", "")
        payment_id = payment_data.get("razorpay_payment_id", "")
        signature = payment_data.get("razorpay_signature", "")

        if not order_id or not payment_id or not signature:
            return False

        # Construct the message: order_id|payment_id
        message = f"{order_id}|{payment_id}"
        key_secret = current_app.config["RAZORPAY_KEY_SECRET"]

        # Generate expected signature
        expected_signature = hmac.new(
            key_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)

    def handle_webhook(self, payload: dict, signature: str) -> dict:
        """Process Razorpay webhook events.

        Handles payment.captured (success) and payment.failed events.

        Args:
            payload: The webhook payload dict from Razorpay.
            signature: The X-Razorpay-Signature header value.

        Returns:
            Dict with status and relevant details.
        """
        event = payload.get("event", "")

        if not self._is_mock_mode():
            # Verify webhook signature
            import json

            webhook_secret = current_app.config.get("RAZORPAY_KEY_SECRET", "")
            payload_str = json.dumps(payload, separators=(",", ":"))
            expected_sig = hmac.new(
                webhook_secret.encode("utf-8"),
                payload_str.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            if not hmac.compare_digest(expected_sig, signature or ""):
                logger.warning("Webhook signature verification failed")
                return {"status": "signature_invalid"}
        else:
            logger.info("[MOCK] Webhook signature verification skipped (mock mode)")

        if event == "payment.captured":
            return self._handle_payment_captured(payload)
        elif event == "payment.failed":
            return self._handle_payment_failed(payload)
        else:
            logger.info(f"Unhandled webhook event: {event}")
            return {"status": "ignored", "event": event}

    def _handle_payment_captured(self, payload: dict) -> dict:
        """Handle a successful payment capture.

        Creates a subscription record and upgrades the user's tier.

        Args:
            payload: The webhook payload.

        Returns:
            Dict with status, user_id, and tier.
        """
        payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})

        # Extract user_id and tier from notes or receipt
        notes = payment_entity.get("notes", {})
        user_id = notes.get("user_id")
        tier = notes.get("tier")

        # Fallback: parse from receipt (format: nyaya_{user_id}_{tier})
        if not user_id or not tier:
            receipt = payment_entity.get("description", "") or ""
            # Try order notes
            order_id = payment_entity.get("order_id")
            if not user_id:
                logger.warning("Could not extract user_id from webhook payload")
                return {"status": "failed", "reason": "missing_user_id"}

        if tier not in self.TIER_AMOUNTS:
            logger.warning(f"Invalid tier in webhook: {tier}")
            return {"status": "failed", "reason": "invalid_tier"}

        # Find the user
        import uuid as uuid_mod

        try:
            uid = uuid_mod.UUID(user_id) if isinstance(user_id, str) else user_id
        except (ValueError, AttributeError):
            logger.warning(f"Invalid user_id in webhook: {user_id}")
            return {"status": "failed", "reason": "invalid_user_id"}

        user = db.session.get(User, uid)
        if not user:
            logger.warning(f"User not found for webhook: {user_id}")
            return {"status": "failed", "reason": "user_not_found"}

        # Create subscription record
        now = datetime.now(timezone.utc)
        subscription = Subscription(
            user_id=uid,
            tier=tier,
            amount_paise=self.TIER_AMOUNTS[tier],
            currency="INR",
            payment_gateway="razorpay",
            gateway_subscription_id=payment_entity.get("order_id"),
            gateway_payment_id=payment_entity.get("id"),
            started_at=now,
            expires_at=now + timedelta(days=30),
            status="active",
        )

        db.session.add(subscription)

        # Update user tier
        user.tier = tier
        db.session.commit()

        logger.info(f"Payment captured: user={user_id}, tier={tier}")
        return {"status": "success", "user_id": str(user_id), "tier": tier}

    def _handle_payment_failed(self, payload: dict) -> dict:
        """Handle a failed payment.

        Logs the failure but does not change the user's tier.

        Args:
            payload: The webhook payload.

        Returns:
            Dict with status="failed".
        """
        payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
        notes = payment_entity.get("notes", {})
        user_id = notes.get("user_id", "unknown")
        error_code = payment_entity.get("error_code", "unknown")
        error_description = payment_entity.get("error_description", "")

        logger.warning(
            f"Payment failed: user={user_id}, error_code={error_code}, "
            f"description={error_description}"
        )

        return {"status": "failed"}

    def check_expiry(self) -> list:
        """Find and downgrade expired subscriptions.

        Queries subscriptions where status='active' and expires_at < now,
        sets status to 'expired', and downgrades user tier to 'free'.

        Returns:
            List of affected user_id strings.
        """
        now = datetime.now(timezone.utc)

        expired_subscriptions = Subscription.query.filter(
            Subscription.status == "active",
            Subscription.expires_at < now,
        ).all()

        affected_user_ids = []

        for sub in expired_subscriptions:
            sub.status = "expired"

            # Downgrade user tier to free
            user = db.session.get(User, sub.user_id)
            if user:
                logger.info(
                    f"Subscription expired: user={user.id}, "
                    f"old_tier={user.tier}, new_tier=free"
                )
                user.tier = "free"
                affected_user_ids.append(str(user.id))

        if affected_user_ids:
            db.session.commit()

        return affected_user_ids
