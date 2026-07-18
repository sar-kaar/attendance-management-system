#!/bin/bash

# Build steps
echo "Building..."
pip install --target="./lib" -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Seed data (optional, won't fail if already seeded)
echo "Seeding data..."
python manage.py seed_data 2>/dev/null || true

echo "Build complete!"
