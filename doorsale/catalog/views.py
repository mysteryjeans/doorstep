from django.conf import settings
from django.http import Http404
from django.core.urlresolvers import reverse

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
        self.categories = list(Category.get_categories())
    
    def get_category(self, **kwargs):
        """
        Returns category from loaded categories
        """
        for category in self.categories:
            is_found = True
            for name, value in kwargs.items():
                if getattr(category, name) != value:
                    is_found = False
                    break
                
            if is_found:
                return category
        
        return None
    
    def get_context_data(self, **kwargs):
        context = super(CatalogBaseView, self).get_context_data(**kwargs)
        
        # Setting data context for catalog base template
        breadcrumbs = ({ 'name': 'Home', 'url': reverse('catalog_index')},)
        if 'breadcrumbs' in context:
            breadcrumbs += context['breadcrumbs']
            
        context['breadcrumbs'] = breadcrumbs    
        context['categories'] = (category for category in self.categories if category.parent is None)
        return context


class IndexView(CatalogBaseView):
    """
    Displays list of featured and recently added products
    """
    template_name = 'catalog/catalog_index.html'
    
    def get(self, request):
        featured_products = Product.get_featured()
        recent_products = Product.get_recent(MAX_RECENT_ARRIVALS)
        
        return super(IndexView, self).get(request,
                                          featured_products=featured_products,
                                          recent_products=recent_products)


class ProductListView(CatalogBaseView):
    """
    Displays list of featured and recently added products
    """
    template_name = 'catalog/category_products.html'
    
    def get(self, request, slug):
        category = self.get_category(slug=slug)
        
        if category is None:
            raise Http404()
        
        products = Product.get_by_category(category)
        
        return super(ProductListView, self).get(request,
                                                category=category,
                                                products=products,
                                                breadcrumbs=category.get_breadcrumbs())


class ProductDetailView(CatalogBaseView):
    """
    Displays product details
    """
    template_name = 'catalog/product.html'
    
    def get(self, request, product_id, slug):
        try:
            product = Product.get_detail(int(product_id))
        except Product.DoesNotExist:
            raise Http404()
        
        return super(ProductDetailView, self).get(request,
                                                  product=product,
                                                  breadcrumbs=product.get_breadcrumbs(self.categories))

