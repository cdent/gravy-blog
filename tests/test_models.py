"""
Simple tests of the models, to get the working.
"""

import pytest

from gravy.models import Blog, Entry

from google.appengine.api import users
from google.appengine.ext.ndb.model import datastore_errors

from .fixtures import data_setup, data_teardown


def setup_module(module):
    module.user_alpha = users.User(email='alpha@example.com')
    module.user_beta = users.User(email='beta@example.com')
    module.testbed = data_setup()


def teardown_module(module):
    data_teardown(testbed)


def test_blog_model():
    title = 'A Blog for Alpha'
    blog = Blog(editors=[user_alpha], title=title)
    blog.put()

    assert blog.created, 'blog failed to get automatic created attribute'
    assert blog.key, 'blog was assigned its own key'

    same_blog = Blog.query(Blog.title == title).get()

    assert same_blog.key == blog.key
    assert same_blog.title == blog.title
    assert same_blog.editors == blog.editors
    assert same_blog.created == blog.created


def test_entry_in_blog():
    blog_title = 'A Blog for Alpha'
    entry_title = 'An entry for Alpha'
    content = '# Oh what a day'
    tags = ['foo', 'bar', 'baz']

    blog = Blog.query(Blog.title == blog_title).get()

    with pytest.raises(datastore_errors.BadValueError):
        entry = Entry()
        entry.put()

    entry = Entry(title=entry_title,
            editor=user_alpha,
            blog=blog.key)

    entry.content = content
    entry.tags = tags

    entry_key = entry.put()

    # did we get the automatic?
    assert entry.created
    assert entry.modified

    entry_dup = entry_key.get()

    assert entry_dup.modified == entry.modified
    assert entry_dup.content == entry.content == content
    assert entry_dup.tags == entry.tags == tags

    entries = Entry.query(Entry.blog == blog.key).order(-Entry.created).fetch()

    assert len(entries) == 1
    assert entries[0].title == entry_title
