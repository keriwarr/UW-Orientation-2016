"""
WSGI config for mathorientation project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application

environment = os.environ.get('DJANGO_ENVIRONMENT', 'development')
settings = 'mathorientation.settings.{}'.format(environment)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

application = get_wsgi_application()
