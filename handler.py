import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airnbn_project.settings')

# Initialize Django
application = get_wsgi_application()

# Vercel handler
def handler(request, context):
    return application(request, context)

# Also provide 'app' for compatibility
app = application
