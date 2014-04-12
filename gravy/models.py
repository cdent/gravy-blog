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

from django.utils.http import urlquote

from .render import render


class Blog(ndb.Model):
    """
    A simple representation of a Blog. It has a title
    and some users that are editors on the blog.
    """
    editors = ndb.UserProperty(repeated=True)
    # XXX: Not immediately obvious how to preserve uniqueness in
    # title.
    title = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_one(cls, blog_title):
        return cls.query(cls.title == blog_title).get()

    def get_absolute_url(self):
        return '/%s' % urlquote(self.title)



class Entry(ndb.Model):
    title = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)
    editor = ndb.UserProperty(required=True)
    content = ndb.TextProperty()
    tags = ndb.StringProperty(repeated=True)
    blog = ndb.KeyProperty(required=True, kind=Blog)

    @classmethod
    def get_one(cls, blog_key, entry_title):
        return cls.query(ndb.AND(
            cls.blog == blog_key,
            cls.title == entry_title)).get()

    @classmethod
    def get_some(cls, blog_key, limit=None):
        return (cls.query(cls.blog == blog_key)
                .order(-Entry.created).fetch(limit))

    def get_absolute_url(self):
        return '/%s/%s' % (urlquote(self.blog.get().title),
                urlquote(self.title))

    @property
    def html(self):
        return render(self.content)
