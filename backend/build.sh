#!/usr/bin/env bash
# Render build script for Nyaya Sutra Backend API

set -o errexit

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Applying database schema..."
# Run schema SQL against the Render PostgreSQL database
# DATABASE_URL is automatically set by Render from the linked database
if [ -n "$DATABASE_URL" ]; then
    python -c "
import os
import psycopg2

db_url = os.environ['DATABASE_URL']
# Render uses 'postgres://' but psycopg2 needs 'postgresql://'
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

conn = psycopg2.connect(db_url)
conn.autocommit = True
cur = conn.cursor()

# Check if tables already exist
cur.execute(\"SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_name = 'courts')\")
tables_exist = cur.fetchone()[0]

if not tables_exist:
    print('Tables not found, applying schema...')
    with open('schema/001_initial_schema.sql', 'r') as f:
        sql = f.read()
        cur.execute(sql)
    print('Schema applied successfully.')
    
    # Apply functions if file exists
    import os.path
    if os.path.isfile('schema/002_functions_and_policies.sql'):
        with open('schema/002_functions_and_policies.sql', 'r') as f:
            sql = f.read()
            cur.execute(sql)
        print('Functions and policies applied.')
else:
    print('Tables already exist, skipping schema.')

cur.close()
conn.close()
"
else
    echo "WARNING: DATABASE_URL not set, skipping schema application."
fi

echo "Build complete."
