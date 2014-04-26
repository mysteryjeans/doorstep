from django.conf import settings
from django.http import Http404

from doorsale.common.views import BaseView
from doorsale.catalog.models import Category, Product


MAX_RECENT_ARRIVALS = getattr(settings, 'MAX_RECENT_ARRIVALS', 10)


class CatalogBaseView(BaseView):
    """
    Generic view for all catalog pages
    """
    def __init__(self, *args, **kwargs):
        super(CatalogBaseView, self).__init__(*args, **kwargs)
        # Loading categories
        self.catagories = list(Category.get_categories())
    
    def get_context_data(self, **kwargs):
        context = super(CatalogBaseView, self).get_context_data(**kwargs)
        
        # Setting data context for catalog base template 
        context['categories'] = (category for category in self.catagories if category.parent is None)
        return context


class IndexView(CatalogBaseView):
    """
    Displays list of featured and recently added products
    """
    template_name = 'catalog/catalog_index.html'
    
    def get(self, request):
        featured_products = Product.get_featured()
        recent_products = Product.get_recent(MAX_RECENT_ARRIVALS)
        
        return self.render(request, self.template_name, {'featured_products': featured_products,
                                                         'recent_products': recent_products })


class ProductListView(CatalogBaseView):
    """
    Displays list of featured and recently added products
    """
    template_name = 'catalog/category_products.html'
    
    def get(self, request, slug):    
        categories = [category for category in self.catagories if category.slug==slug]
        if not len(categories):
            raise Http404()
        
        category = categories[0]
        products = Product.get_by_category(category)
        
        return self.render(request, self.template_name, {'category': category, 'products': products})


