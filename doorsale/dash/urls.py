from django.conf.urls import patterns, url

from doorsale.dash.views import IndexView

urlpatterns = patterns(
  '',
  url(r'^$', IndexView.as_view(), name='dash_index'),
  )
