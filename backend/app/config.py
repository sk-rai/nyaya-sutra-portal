"""Environment-based configuration classes for the Nyaya Sutra Backend API."""

import os


class BaseConfig:
    """Base configuration shared across all environments."""

    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour in seconds

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://nyaya_app:NyayaSutra2026!@localhost:5432/nyaya_sutra",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGIN = os.getenv("CORS_ORIGIN", "https://sk-rai.github.io")

    # Razorpay
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

    # OTP delivery
    OTP_EMAIL_SERVICE = os.getenv("OTP_EMAIL_SERVICE", "")
    OTP_SMS_SERVICE = os.getenv("OTP_SMS_SERVICE", "")

    # Redis (for rate limiting in multi-instance deployment)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Tier configuration
    TIER_CONFIG = {
        "free": {
            "max_tracked_cases": 5,
            "daily_searches": 10,
            "refresh_hours": 48,
            "synopsis_access": False,
        },
        "individual": {
            "max_tracked_cases": 50,
            "daily_searches": 50,
            "refresh_hours": 24,
            "synopsis_access": False,
        },
        "advocate_normal": {
            "max_tracked_cases": 300,
            "daily_searches": 200,
            "refresh_hours": 24,
            "synopsis_access": False,
        },
        "advocate_premium": {
            "max_tracked_cases": 2000,
            "daily_searches": None,  # Unlimited
            "refresh_hours": 12,
            "synopsis_access": True,
        },
    }

    # Razorpay tier amounts in paise
    TIER_AMOUNTS = {
        "individual": 5000,        # ₹50
        "advocate_normal": 19900,  # ₹199
        "advocate_premium": 59900, # ₹599
    }


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    ENABLE_SCHEDULER = True


class TestingConfig(BaseConfig):
    """Testing environment configuration."""

    TESTING = True
    DEBUG = True
    ENABLE_SCHEDULER = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://nyaya_app:NyayaSutra2026!@localhost:5432/nyaya_sutra_test",
    )
    JWT_SECRET_KEY = "test-secret-key"
    CORS_ORIGIN = "*"


class ProductionConfig(BaseConfig):
    """Production environment configuration."""

    DEBUG = False
    SQLALCHEMY_ECHO = False
    ENABLE_SCHEDULER = True


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
