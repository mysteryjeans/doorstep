

############################################
# Doorsale urls containing urls for all apps
urlpatterns += patterns('',
                        url(r'^', include('doorsale.urls')),
)

# In Debug mode we need to serve media files
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


################### OR #####################
# You adjust each app urls according to your preferences
# urlpatterns += patterns('',
#     # Doorsale apps urls
#     url(r'^', include('doorsale.catalog.urls')),
#     url(r'^accounts/', include('doorsale.accounts.urls')),
#     url(r'^sales/', include('doorsale.sales.urls')),
#     url(r'^payments/', include('doorsale.payments.urls')),
#     url(r'^pages/', include('doorsale.pages.urls'))
# )
