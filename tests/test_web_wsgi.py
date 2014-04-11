"""
Run simple tests to see if we can load pages off the
WSGI app.
"""

from wsgi_intercept import requests_intercept
import wsgi_intercept

import requests

from google.appengine.api import users

from main import app
from gravy.models import Blog, Entry

from .fixtures import data_setup, data_teardown



def setup_module(module):
    module.testbed = data_setup()
    requests_intercept.install()
    def app_fn(): return app
    wsgi_intercept.add_wsgi_intercept('localhost', 8000, app_fn)

    module.user_alpha = users.User(email='alpha@example.com')


def teardown_module(module):
    data_teardown(testbed)
    requests_intercept.uninstall()


def test_request_home():
    url = 'http://localhost:8000/'
    title = 'Fantastic'

    response = requests.get(url)

    assert response.status_code == 200
    assert '<h1>Welcome to Gravy Blog</h1>' in response.text
    assert '<ul class="blogs">' in response.text
    assert '<a class="blog"' not in response.text

    blog = Blog(editors=[user_alpha], title=title)
    blog_key = blog.put()
    response = requests.get(url)

    assert response.status_code == 200
    assert '<h1>Welcome to Gravy Blog</h1>' in response.text
    assert '<ul class="blogs">' in response.text
    assert '<a class="blog" href="Fantastic">' in response.text


def test_no_blog():
    url = 'http://localhost:8000/Snap'

    response = requests.get(url)
    assert response.status_code == 404


def test_blog_summary():
    url = 'http://localhost:8000/Fantastic'

    response = requests.get(url)
    assert response.status_code == 200
    assert '<h1>Fantastic</h1>' in response.text
    assert '<section class="entries">' in response.text
    assert '<article class="entry">' not in response.text

    blog = Blog.query(Blog.title == 'Fantastic').get()
    entry = Entry(title = 'My First Entry',
            editor = user_alpha,
            blog = blog.key)
    entry.content = '<p>What do you know?</p>'
    entry.tags = ['firstpost']
    entry.put()

    response = requests.get(url)
    assert response.status_code == 200
    assert '<h1>Fantastic</h1>' in response.text
    assert '<section class="entries">' in response.text
    assert '<article class="entry">' in response.text
    assert '<h1>My First Entry</h1>' in response.text
    assert '<p>What do you know?</p>' in response.text
