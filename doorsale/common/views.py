from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView


class BaseView(TemplateView):
    """
    Base view for all Doorsale views
    """
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        
        # Settings context data for base template
        context['SITE_NAME'] = settings.SITE_NAME
        context['SITE_TITLE'] = settings.SITE_TITLE
        context['SITE_DESCRIPTION'] = settings.SITE_DESCRIPTION
        context['COPYRIGHT'] = settings.COPYRIGHT
        context['CONTACT_EMAIL'] = settings.CONTACT_EMAIL
        
        return context        
