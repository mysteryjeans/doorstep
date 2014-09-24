from django.conf.urls import patterns, url

from doorsale.pages.views import BasePageView

urlpatterns = patterns('',
                       url(r'^(?P<slug>[\w-]+)/$', BasePageView.as_view(), name='pages_page_view'),
                       )
