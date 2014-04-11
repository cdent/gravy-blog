from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'gravy.views.home'),
    (r'^editor$', 'gravy.views.editor'),
    (r'^creator$', 'gravy.views.creator'),
    (r'^(?P<blog_title>[^/]+)/?$', 'gravy.views.summary'),
    (r'^(?P<blog_title>[^/]+)/(?P<entry_title>[^/]+)/?$', 'gravy.views.entry'),
)
