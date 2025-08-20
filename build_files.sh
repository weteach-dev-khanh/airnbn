#!/bin/bash

# Build script for Vercel deployment
echo "Starting Vercel build..."

# Install requirements
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Create staticfiles directory
echo "Creating static files directory..."
mkdir -p staticfiles

# Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear

# Run migrations
echo "Running migrations..."
python3.9 manage.py migrate --noinput

echo "Build completed successfully!"