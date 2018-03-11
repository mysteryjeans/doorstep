"""
Accounts views for Doorstep apps
"""

from django.db import transaction
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template.loader import get_template

from doorstep.views import BaseView
from doorstep.exceptions import DoorstepError
from doorstep.decorators import anonymous_required
from doorstep.catalog.views import CatalogBaseView
from doorstep.accounts.forms import RegisterForm, PasswordResetForm, ChangePasswordForm
from doorstep.utils.helpers import send_mail


User = get_user_model()


class LoginView(CatalogBaseView):
    """
    Login view for Doorstep
    """
    template_name = 'accounts/login.html'
    decorators = [anonymous_required]

    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get('next', '')
        return super(LoginView, self).get_context_data(next_url=next_url, **kwargs)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if '@' in username:
            try:
                user = User.objects.get(email__iexact=username)
                username = user.username
            except User.DoesNotExist:
                pass

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
    Logout view from Doorstep
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
    decorators = [transaction.atomic, anonymous_required]

    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get('next', '')
        return super(RegisterView, self).get_context_data(next_url=next_url, **kwargs)

    def get(self, request):
        form = RegisterForm()
        as_superuser = User.objects.count() == 0
        return super(RegisterView, self).get(request, form=form, as_superuser=as_superuser)

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

                success = 'Thank you for sign up, you have been also successfully logged in, <strong>lets explore!</strong>'
            except ValidationError as e:
                error = e.message

        return super(RegisterView, self).get(request, form=form, error=error, success=success)


class ForgotPasswordView(CatalogBaseView):
    """
    Password recovery view
    """
    template_name = 'accounts/forgot_password.html'
    decorators = [anonymous_required]
    page_title = 'Forgot password'

    def post(self, request):
        error = None
        success = None
        email = request.POST.get('email', None)

        if email:
            email = email.strip()
            try:
                user = User.objects.get_reset_code(email)

                # Sending password reset link email to user
                context = Context({'user': user, 'SITE_NAME': self.get_config('SITE_NAME'), 'DOMAIN': self.get_config('DOMAIN')})
                msg_subject = get_template("accounts/email/password_reset_subject.txt").render(context)
                context = Context({'user': user, 'SITE_NAME': self.get_config('SITE_NAME'), 'DOMAIN': self.get_config('DOMAIN')})
                msg_text = get_template("accounts/email/password_reset.html").render(context)
                to_email = '%s <%s>' % (user.get_full_name(), user.email)
                send_mail(msg_subject, msg_text, [to_email], True)

                success = 'Password reset intructions has been sent to your email address.'
            except DoorstepError as e:
                error = e.message

        return self.get(request, error=error, success=success)


class PasswordResetView(CatalogBaseView):
    """
    Password recovery view
    """
    page_title = 'Password reset'
    template_name = 'accounts/password_reset.html'
    decorators = [anonymous_required]

    def get(self, request, user_id, reset_code):
        form = PasswordResetForm()
        return super(PasswordResetView, self).get(request, form=form, user_id=user_id, reset_code=reset_code)

    def post(self, request, user_id, reset_code):
        error = None
        success = None
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            try:
                User.objects.reset_password(user_id, reset_code, data['password'])
                success = 'Your password has been successfully reset!'
            except DoorstepError as e:
                error = e.message

        return super(PasswordResetView, self).get(request, form=form, user_id=user_id, reset_code=reset_code,
                                                  error=error, success=success)


class ChangePasswordView(CatalogBaseView):
    """
    Password recovery view
    """
    page_title = 'Change password'
    template_name = 'accounts/change_password.html'
    decorators = [login_required]

    def get(self, request):
        form = ChangePasswordForm()
        return super(ChangePasswordView, self).get(request, form=form)

    def post(self, request):
        error = None
        success = None
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            try:
                User.objects.change_password(request.user, data['current_password'], data['password'])
                success = 'Your password has been successfully changed!'
            except DoorstepError as e:
                error = e.message

        return super(ChangePasswordView, self).get(request, form=form, error=error, success=success)
