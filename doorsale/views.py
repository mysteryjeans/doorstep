from django.conf import settings
from django.views.generic import TemplateView


class BaseView(TemplateView):
    """
    Base view for all Doorsale views
    
    Provide site context variables from settings and apply decoractors to views
    """
    
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        
        # Settings context data for base template
        context['SITE_NAME'] = settings.SITE_NAME
        context['SITE_TITLE'] = settings.SITE_TITLE
        context['SITE_DESCRIPTION'] = settings.SITE_DESCRIPTION
        context['COPYRIGHT'] = settings.COPYRIGHT
        context['CONTACT_EMAIL'] = settings.CONTACT_EMAIL
        context['app_user'] = self.request.user
        
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