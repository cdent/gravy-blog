"""
URLs for the APP:

    /            GET home/root page
    /editor      GET and POST an entry edit
    /creator     GET and POST a blog creation
    /blog_title  GET blog summary
    /blog_title/entry_title GET blog entry
"""

from django.conf.urls.defaults import patterns


# Order matters.
urlpatterns = patterns('',
    (r'^$', 'gravy.views.home'),
    (r'^editor$', 'gravy.views.editor'),
    (r'^creator$', 'gravy.views.creator'),
    (r'^(?P<blog_title>[^/]+)/?$', 'gravy.views.summary'),
    (r'^(?P<blog_title>[^/]+)/(?P<entry_title>[^/]+)/?$', 'gravy.views.entry'),
)
