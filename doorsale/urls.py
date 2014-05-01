import sales.urls
import catalog.urls
import accounts.urls

from django.contrib import admin
from django.conf.urls import patterns, include, url


admin.autodiscover()


# Doorsale apps urls
urlpatterns = patterns('',
    url(r'^', include(catalog.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^sales/', include(sales.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
