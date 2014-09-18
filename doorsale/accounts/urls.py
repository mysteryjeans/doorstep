from django.conf.urls import patterns, url

from doorsale.accounts.views import LoginView, LogoutView, RegisterView, ForgotPasswordView

urlpatterns = patterns('',
                       url(r'^login/$', LoginView.as_view(), name='accounts_login'),
                       url(r'^logout/$', LogoutView.as_view(), name='accounts_logout'),
                       url(r'^register/$', RegisterView.as_view(), name='accounts_register'),
                       url(r'^forgot_password/$', ForgotPasswordView.as_view(), name='accounts_forgot_password'),
                       )
