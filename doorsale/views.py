from django.views.generic import TemplateView
from django.core.exceptions import ImproperlyConfigured

from doorsale.models import SysConfig


class BaseView(TemplateView):
    """
    Base view for all Doorsale views

    Provide site context variables from settings and apply decoractors to views
    """

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        # Settings context data for base template
        context['app_user'] = self.request.user
        context['request'] = self.request
        context['SITE_NAME'] = self.get_config('SITE_NAME')
        context['SITE_TITLE'] = self.get_config('SITE_TITLE')
        context['SITE_DESCRIPTION'] = self.get_config('SITE_DESCRIPTION')
        context['COPYRIGHT'] = self.get_config('COPYRIGHT')
        context['SUPPORT_EMAIL'] = self.get_config('SUPPORT_EMAIL')

        if hasattr(self, 'page_title'):
            context['page_title'] = self.page_title

        return context

    @classmethod
    def as_view(cls, **initkwargs):
        """
        Returns view function

        Decorators will be applied defined at class level
        """
        view = super(BaseView, cls).as_view(**initkwargs)

        if hasattr(cls, 'decorators'):
            for decorator in cls.decorators:
                view = decorator(view)

        return view

    @staticmethod
    def get_config(name):
        return SysConfig.get_config(name)
