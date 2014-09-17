

############################################
# Doorsale urls containing urls for all apps
urlpatterns += patterns('',
    url(r'^', include('doorsale.urls')),
)

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
