from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'gravy.views.home'),
    (r'^(?P<blog_title>\w+)/?$', 'gravy.views.summary'),
    (r'^(?P<blog_title>\w+)/(?P<entry_entry>\w+)/?$', 'gravy.views.entry'),
    (r'^editor$', 'gravy.views.editor')
)
