from django.conf.urls import url

from doorsale.dash.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='dash_index'),
]
