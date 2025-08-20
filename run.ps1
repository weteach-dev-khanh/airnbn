# PowerShell script to run Django Airbnb project with MongoDB

Write-Host "Starting Django Airbnb project with MongoDB..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Build and start the containers
Write-Host "Building Docker containers..." -ForegroundColor Yellow
docker-compose build

Write-Host "Starting MongoDB service..." -ForegroundColor Yellow
docker-compose up -d mongodb

Write-Host "Waiting for MongoDB to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "Starting Django application..." -ForegroundColor Yellow
docker-compose up web

Write-Host "Application should be available at http://localhost:8000" -ForegroundColor Green
