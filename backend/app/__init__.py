"""Flask application factory."""

from flask import Flask, jsonify

from .config import config_by_name
from .extensions import cors, db, jwt
from .middleware.error_handler import register_error_handlers


def create_app(config_name=None):
    """Create and configure the Flask application.

    Args:
        config_name: Configuration environment name (development, testing, production).
                     Defaults to 'development' if not specified.

    Returns:
        Configured Flask application instance.
    """
    if config_name is None:
        config_name = "development"

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(
        app,
        origins=[app.config["CORS_ORIGIN"]],
        supports_credentials=True,
        allow_headers=["Authorization", "Content-Type"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # JWT error handlers to use standard envelope format
    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        from .utils.response import error_response
        return error_response(
            code="UNAUTHORIZED",
            message="Authentication required. Please provide a valid token.",
            status=401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        from .utils.response import error_response
        return error_response(
            code="UNAUTHORIZED",
            message="Invalid token. Please login again.",
            status=401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        from .utils.response import error_response
        return error_response(
            code="UNAUTHORIZED",
            message="Token has expired. Please login again.",
            status=401,
        )

    # Import models so they are registered with SQLAlchemy metadata
    from . import models  # noqa: F401

    # Register global error handlers
    register_error_handlers(app)

    # Register API blueprints
    from .api.auth import auth_bp
    from .api.courts import courts_bp
    from .api.cases import cases_bp
    from .api.tracking import tracking_bp
    from .api.relationships import relationships_bp
    from .api.subscriptions import subscriptions_bp
    from .api.synopsis import synopsis_bp
    from .api.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(courts_bp)
    app.register_blueprint(cases_bp)
    app.register_blueprint(tracking_bp)
    app.register_blueprint(relationships_bp)
    app.register_blueprint(subscriptions_bp)
    app.register_blueprint(synopsis_bp)
    app.register_blueprint(admin_bp)

    # Ensure all responses have JSON Content-Type
    @app.after_request
    def set_json_content_type(response):
        if response.content_type == "application/json":
            return response
        # Only override for API routes that return JSON
        if response.mimetype == "application/json":
            response.headers["Content-Type"] = "application/json"
        return response

    # Health check endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint returning app status."""
        from flask import jsonify

        return jsonify({
            "success": True,
            "data": {
                "status": "healthy",
                "version": "1.0.0",
            },
            "error": None,
        })

    # Optionally start background scheduler (not during testing)
    if not app.config.get("TESTING", False):
        # Only start scheduler if ENABLE_SCHEDULER is set (avoids double-start with gunicorn)
        if app.config.get("ENABLE_SCHEDULER", False):
            from .jobs.scheduler import init_scheduler
            init_scheduler(app)

    return app
