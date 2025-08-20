#!/bin/bash

echo "Starting Django Airbnb project with MongoDB..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start the containers
echo "Building Docker containers..."
docker-compose build

echo "Starting services..."
docker-compose up -d mongodb

echo "Waiting for MongoDB to be ready..."
sleep 10

echo "Starting Django application..."
docker-compose up web

echo "Application should be available at http://localhost:8000"
