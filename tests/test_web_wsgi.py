"""
Run simple tests to see if we can load pages off the
WSGI app.
"""

from wsgi_intercept import requests_intercept
import wsgi_intercept

import requests

from main import app

from .fixtures import data_setup, data_teardown


def setup_module(module):
    module.testbed = data_setup()
    requests_intercept.install()
    def app_fn(): return app
    wsgi_intercept.add_wsgi_intercept('localhost', 8000, app_fn)


def teardown_module(module):
    data_teardown(testbed)
    requests_intercept.uninstall()


def test_request_root():
    url = 'http://localhost:8000/'

    response = requests.get(url)

    # no views yet

