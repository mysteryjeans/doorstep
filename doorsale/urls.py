from django.conf.urls import patterns, include, url


# Doorsale apps urls
urlpatterns = patterns('',
                       url(r'^', include('doorsale.catalog.urls')),
                       url(r'^accounts/', include('doorsale.accounts.urls')),
                       url(r'^sales/', include('doorsale.sales.urls')),
                       url(r'^payments/', include('doorsale.payments.urls')),
                       url(r'^pages/', include('doorsale.pages.urls'))
                       )
