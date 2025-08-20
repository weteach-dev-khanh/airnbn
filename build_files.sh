#!/bin/bash

# Build script for Vercel deployment
echo "Building for Vercel..."
pip install -r requirements.txt
echo "Installing Django dependencies..."
# Collect static files
python manage.py collectstatic --noinput
echo "Collecting static files..."
# Run migrations
python manage.py migrate --noinput
echo "Running migrations..."
echo "Build completed successfully."