from django.shortcuts import get_object_or_404

from doorsale.views import BaseView
from doorsale.catalog.views import CatalogBaseView
from doorsale.pages.models import FlatPage


class BasePageView(BaseView):
    """
    Renders flat page under BaseView
    """
    template_name = 'pages/base_page.html'

    def get(self, request, page_url):
        page = get_object_or_404(FlatPage, url=page_url, is_active=True)

        return super(BasePageView, self).get(request, page_title=page.title, page=page)


class CatalogPageView(CatalogBaseView):
    """
    Renders flat page under CatalogBaseView
    """
    template_name = 'pages/catalog_page.html'

    def get(self, request, page_url):
        page = get_object_or_404(FlatPage, url=page_url, is_active=True)
        breadcrumbs = ({'name': page.title, 'url': page.get_absolute_url()},)

        return super(CatalogPageView, self).get(request, page_title=page.title, page=page, breadcrumbs=breadcrumbs)
