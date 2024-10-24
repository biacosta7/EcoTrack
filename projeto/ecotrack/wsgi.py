"""
WSGI config for ecotrack project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecotrack.settings')
print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'))

application = get_wsgi_application()
logging.info(f'DJANGO_SETTINGS_MODULE: {os.environ.get("DJANGO_SETTINGS_MODULE")}')
