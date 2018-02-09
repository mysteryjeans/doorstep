from django.conf.urls import include, url


# Doorstep apps urls
urlpatterns = [
    url(r'^', include('doorstep.catalog.urls')),
    url(r'^accounts/', include('doorstep.accounts.urls')),
    url(r'^sales/', include('doorstep.sales.urls')),
    url(r'^payments/', include('doorstep.payments.urls')),
    url(r'^pages/', include('doorstep.pages.urls'))
]
