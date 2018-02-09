from django.conf.urls import url

from doorstep.pages.views import BasePageView

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', BasePageView.as_view(), name='pages_page_view'),
]
