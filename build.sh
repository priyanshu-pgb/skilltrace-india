#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files with whitenoise
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Seed demonstration data
python manage.py seed_demo_data
