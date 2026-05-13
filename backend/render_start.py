"""Render-compatible startup script.

Handles the postgres:// → postgresql:// URL fix that Render requires,
then creates the Flask app for gunicorn.
"""

import os

# Fix Render's DATABASE_URL format (postgres:// → postgresql://)
database_url = os.environ.get("DATABASE_URL", "")
if database_url.startswith("postgres://"):
    os.environ["DATABASE_URL"] = database_url.replace("postgres://", "postgresql://", 1)

from app import create_app

app = create_app(os.getenv("FLASK_ENV", "production"))
