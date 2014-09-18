"""
Accounts views for Doorsale apps
"""

from django.db import transaction
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model, authenticate, login, logout

from doorsale.views import BaseView
from doorsale.decorators import anonymous_required
from doorsale.catalog.views import CatalogBaseView
from doorsale.accounts.forms import RegisterForm


User = get_user_model()


class LoginView(CatalogBaseView):

    """
    Login view for Doorsale
    """
    template_name = 'accounts/login.html'
    decorators = [anonymous_required]

    def get_context_data(self, **kwargs):
        next_url = self.request.REQUEST.get('next', '')
        breadcrumbs = ({'name': 'Login', 'url': reverse('accounts_login')},)
        return super(LoginView, self).get_context_data(breadcrumbs=breadcrumbs, next_url=next_url, **kwargs)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.POST.get('next', reverse('catalog_index')))
            else:
                error = ('Your account has been disabled. We apologize for any inconvenience! If this is a mistake'
                         ' please contact our <a href="mailto:%s">support</a>.') % settings.SUPPORT_EMAIL
        else:
            error = ('Username and password didn\'t matched, if you forgot your password?'
                     ' <a href="%s">Request new one</a>') % reverse('accounts_forgot_password')

        return super(LoginView, self).get(request, error=error)


class LogoutView(BaseView):

    """
    Logout view from Doorsale
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


class RegisterView(CatalogBaseView):

    """
    User registration view
    """
    page_title = 'Register'
    template_name = "accounts/register.html"
    decorators = [transaction.commit_on_success, anonymous_required]

    def get_context_data(self, **kwargs):
        next_url = self.request.REQUEST.get('next', '')
        breadcrumbs = ({'name': 'Register', 'url': reverse('accounts_register')},)
        return super(RegisterView, self).get_context_data(breadcrumbs=breadcrumbs, next_url=next_url, **kwargs)

    def get(self, request):
        form = RegisterForm()
        return super(RegisterView, self).get(request, form=form)

    def post(self, request):
        error = None
        success = None
        form = RegisterForm(request.POST)

        if form.is_valid():
            try:
                data = form.cleaned_data
                User.objects.register(data['first_name'], data['last_name'], data['email'],
                                      data['gender'], data['username'], data['password'])

                # Login registered user automatically
                # Binding propery backend to user model
                user = authenticate(username=data['username'], password=data['password'])
                login(request, user)

                next_url = request.POST.get('next', None)
                if next_url:
                    return HttpResponseRedirect(next_url)

                success = ('You have register successfully, please continue to browse our'
                           ' <a href="%s">catalog</a>.') % reverse('catalog_index')
            except ValidationError as e:
                error = e.message

        return super(RegisterView, self).get(request, form=form, error=error, success=success)


class ForgotPasswordView(CatalogBaseView):

    """
    Password recovery view
    """
    template_name = 'accounts'
    decorators = [anonymous_required]
