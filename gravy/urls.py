from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'gravy.views.home'),
    (r'^editor$', 'gravy.views.editor'),
    (r'^creator$', 'gravy.views.creator'),
    (r'^(?P<blog_title>[\w%]+)/?$', 'gravy.views.summary'),
    (r'^(?P<blog_title>[\w%]+)/(?P<entry_title>[\w%]+)/?$', 'gravy.views.entry'),
)
