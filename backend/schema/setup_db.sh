#!/bin/bash
# ============================================================
# Nyaya Sutra - Database Setup Script
# Creates a SEPARATE database and user (no interference with trustcapture)
# ============================================================

set -e

echo "=== Nyaya Sutra Database Setup ==="
echo ""

# Create dedicated user for nyaya sutra
echo "Creating user 'nyaya_app'..."
sudo -u postgres psql -c "DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'nyaya_app') THEN
        CREATE ROLE nyaya_app WITH LOGIN PASSWORD 'NyayaSutra2026!';
    END IF;
END
\$\$;"

# Create dedicated database
echo "Creating database 'nyaya_sutra'..."
sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname = 'nyaya_sutra'" | grep -q 1 || \
    sudo -u postgres createdb nyaya_sutra -O nyaya_app

# Grant privileges ONLY on nyaya_sutra database
echo "Granting privileges..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE nyaya_sutra TO nyaya_app;"
sudo -u postgres psql -c "REVOKE ALL ON DATABASE trustcapture_db FROM nyaya_app;" 2>/dev/null || true
sudo -u postgres psql -c "REVOKE ALL ON DATABASE trustcapture_test FROM nyaya_app;" 2>/dev/null || true
sudo -u postgres psql -c "REVOKE ALL ON DATABASE test_trustcapture FROM nyaya_app;" 2>/dev/null || true

# Run schema files
echo "Running schema migrations..."
sudo -u postgres psql -d nyaya_sutra -f /home/lynksavvy/projects/nyaya-sutra-portal/backend/schema/001_initial_schema.sql
sudo -u postgres psql -d nyaya_sutra -f /home/lynksavvy/projects/nyaya-sutra-portal/backend/schema/002_functions_and_policies.sql

# Grant schema permissions to nyaya_app
echo "Granting table permissions to nyaya_app..."
sudo -u postgres psql -d nyaya_sutra -c "GRANT ALL ON ALL TABLES IN SCHEMA public TO nyaya_app;"
sudo -u postgres psql -d nyaya_sutra -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO nyaya_app;"
sudo -u postgres psql -d nyaya_sutra -c "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO nyaya_app;"
sudo -u postgres psql -d nyaya_sutra -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO nyaya_app;"
sudo -u postgres psql -d nyaya_sutra -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO nyaya_app;"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Database: nyaya_sutra"
echo "User: nyaya_app"
echo "Password: NyayaSutra2026!"
echo "Host: localhost"
echo "Port: 5432"
echo ""
echo "Connection string:"
echo "  postgresql://nyaya_app:NyayaSutra2026!@localhost:5432/nyaya_sutra"
echo ""
echo "Verify with:"
echo "  psql -U nyaya_app -d nyaya_sutra -h localhost -c '\dt'"
echo ""
echo "NOTE: This database is completely isolated from trustcapture_db."
