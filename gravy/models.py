"""
Models for our blog. We'll use Google's ndb as that provides
automatic caching and highly resilient storage.

We're storing UserProperties directly, which is not considered
entirely safe because there is a chance a user will change
their email address. AppEngine documentation simultaneously
warns about this problems and then uses the technique all over
the place. Used here for brevity.
"""

from google.appengine.ext import ndb


class Blog(ndb.Model):
    """
    A simple representation of a Blog. It has a title
    and some users that are editors on the blog.
    """
    editors = ndb.UserProperty(repeated=True)
    title = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)


class Entry(ndb.Model):
    title = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    editor = ndb.UserProperty(required=True)
    content = ndb.TextProperty()
    tags = ndb.StringProperty(repeated=True)
    blog = ndb.KeyProperty(required=True, kind=Blog)
