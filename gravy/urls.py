from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'gravy.views.home'),
    (r'^(?P<blog>\w+)/?$', 'gravy.views.summary'),
    (r'^(?P<blog>\w+)/(?P<entry>\w+)/?$', 'gravy.views.entry'),
    (r'^editor$', 'gravy.views.editor')
)
