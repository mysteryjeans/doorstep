from django.conf.urls import patterns, include, url

urlpatterns = patterns('doorsale.catalog.views',
                       url(r'^$', 'index', name='index'),
)
