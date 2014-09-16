import sales.urls
import pages.urls
import catalog.urls
import accounts.urls
import payments.urls

from django.contrib import admin
from django.conf.urls import patterns, include, url


admin.autodiscover()


# Doorsale apps urls
urlpatterns = patterns('',
    url(r'^', include(catalog.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^sales/', include(sales.urls)),
    url(r'^payments/', include(payments.urls)),
    url(r'^pages/', include(pages.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
