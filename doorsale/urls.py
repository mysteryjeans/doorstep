from django.conf.urls import include, url


# Doorsale apps urls
urlpatterns = [
    url(r'^', include('doorsale.catalog.urls')),
    url(r'^accounts/', include('doorsale.accounts.urls')),
    url(r'^sales/', include('doorsale.sales.urls')),
    url(r'^payments/', include('doorsale.payments.urls')),
    url(r'^pages/', include('doorsale.pages.urls'))
]
