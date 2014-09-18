"""
Decorators for Doorsale accounts app
"""

from functools import wraps
from django.conf import settings
from django.http import HttpResponseRedirect


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
