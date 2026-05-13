"""Entry point for the Nyaya Sutra Backend API."""

import os

from dotenv import load_dotenv

load_dotenv()

# Fix Render's DATABASE_URL format (postgres:// → postgresql://)
database_url = os.environ.get("DATABASE_URL", "")
if database_url.startswith("postgres://"):
    os.environ["DATABASE_URL"] = database_url.replace("postgres://", "postgresql://", 1)

from app import create_app

app = create_app(os.getenv("FLASK_ENV", "development"))

if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", 5000)),
        debug=app.config.get("DEBUG", False),
    )
