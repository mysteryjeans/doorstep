"""
Generic doorsale views decorators
"""

from functools import wraps
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def anonymous_required(view_func):
    """
    Decorator for views that checks that the user is not logged.
    """
    @wraps(view_func)
    def check_anonymous(request, *args, **kwargs):
        if request.user.is_anonymous():
            return view_func(request, *args, **kwargs)

        next_url = request.GET.get('next', None)
        return HttpResponseRedirect(next_url if next_url else settings.LOGIN_REDIRECT_URL)

    return check_anonymous


def staff_member_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """
    @wraps(view_func)
    def check_staff(request, *args, **kwargs):
        user = request.user
        if user.is_active and user.is_staff:
            return view_func(request, *args, **kwargs)

        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return login_required(check_staff)
