#!/bin/bash

# Build script for Vercel deployment
echo "Starting Vercel build..."

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
python3.9 manage.py migrate --noinput

echo "Build completed successfully!"