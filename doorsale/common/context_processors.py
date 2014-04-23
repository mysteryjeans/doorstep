from django.conf import settings



def bootstrip(request):
    """
    Setting basic context variables
    """
    return {
            'SITE_NAME': settings.SITE_NAME,
            'SITE_TITLE': settings.SITE_TITLE,
            'SITE_DESCRIPTION': settings.SITE_DESCRIPTION,
            'COPYRIGHT': settings.COPYRIGHT,
            'CONTACT_EMAIL': settings.CONTACT_EMAIL
    }