#!/usr/bin/env python3
"""
Vercel build script for Django application
"""
import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and handle errors"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def main():
    """Main build function"""
    print("Starting Vercel build process...")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airnbn_project.settings')
    
    # Install dependencies
    print("Installing dependencies...")
    run_command("pip install -r requirements.txt")
    
    # Collect static files
    print("Collecting static files...")
    run_command("python manage.py collectstatic --noinput")
    
    # Run migrations
    print("Running database migrations...")
    run_command("python manage.py migrate --noinput")
    
    print("Build completed successfully!")

if __name__ == "__main__":
    main()
