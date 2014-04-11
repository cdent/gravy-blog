"""
main.py provides the app callable to the AppEngine.
"""

import os

from django.core.handlers.wsgi import WSGIHandler


# This _must_ be set somewhere and here seems to work.
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


app = WSGIHandler()
