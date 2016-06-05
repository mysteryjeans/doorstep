from __future__ import unicode_literals

from django.views.generic import TemplateView

from doorsale.models import SysConfig


class BaseView(TemplateView):
    """
    Base view for all Doorsale views

    Provide site context variables from settings and apply decoractors to views
    """
    # Pipeline CSS style package name
    style_name = 'base'

    # Base template to extend in drived views
    base_template_name = 'doorsale/base.html'

    # Decorators applied to generated view
    decorators = []

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        # Settings context data for base template
        context['cache_timeout'] = 300
        context['request'] = self.request
        context['style_name'] = self.style_name
        context['base_template_name'] = self.base_template_name
        context['SITE_NAME'] = self.get_config('SITE_NAME')
        context['SITE_TITLE'] = self.get_config('SITE_TITLE')
        context['SITE_DESCRIPTION'] = self.get_config('SITE_DESCRIPTION')
        context['COPYRIGHT'] = self.get_config('COPYRIGHT')
        context['SUPPORT_EMAIL'] = self.get_config('SUPPORT_EMAIL')

        if hasattr(self, 'page_title'):
            context['page_title'] = self.page_title

        return context

    @classmethod
    def get_decorators(cls):
        """
        Returns list of decorators defined as attribute of class

        Generic base views should override get_decorators method instead of defining decorators attribute
        """
        return cls.decorators

    @classmethod
    def as_view(cls, **initkwargs):
        """
        Returns view function

        Decorators will be applied defined at class level
        """
        view = super(BaseView, cls).as_view(**initkwargs)

        # Applying decorators to generated view
        for decorator in cls.get_decorators():
            view = decorator(view)

        return view

    @staticmethod
    def get_config(name):
        return SysConfig.get_config(name)
