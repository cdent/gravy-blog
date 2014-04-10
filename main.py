"""
main.py provides the app callable to the AppEngine.
"""

from django.core.handlers.wsgi import WSGIHandler


app = WSGIHandler()
