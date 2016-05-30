from django.conf.urls import url

from doorsale.accounts.views import LoginView, LogoutView, RegisterView, ForgotPasswordView, PasswordResetView, ChangePasswordView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='accounts_login'),
    url(r'^logout/$', LogoutView.as_view(), name='accounts_logout'),
    url(r'^register/$', RegisterView.as_view(), name='accounts_register'),
    url(r'^forgot_password/$', ForgotPasswordView.as_view(), name='accounts_forgot_password'),
    url(r'^change_password/$', ChangePasswordView.as_view(), name='accounts_change_password'),
    url(r'^password_reset/(?P<user_id>\d+)-(?P<reset_code>\w+)/$',
        PasswordResetView.as_view(), name='accounts_password_reset'),
]
