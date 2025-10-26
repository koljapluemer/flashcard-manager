#!/usr/bin/env bash
set -o errexit

# Install dependencies via Poetry
poetry install --no-root --only main

# Run management commands inside Poetry environment
poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate
