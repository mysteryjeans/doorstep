import urllib

from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View

from doorsale.views import BaseView
from doorsale.catalog.forms import AdvanceSearchForm
from doorsale.catalog.models import Manufacturer, Category, Product
from doorsale.financial.models import Currency


MAX_RECENT_ARRIVALS = getattr(settings, 'MAX_RECENT_ARRIVALS', 10)


class CatalogBaseView(BaseView):
    """
    Generic view for all catalog pages
    """
    def __init__(self, *args, **kwargs):
        super(CatalogBaseView, self).__init__(*args, **kwargs)
        # Loading categories
        self.categories = Category.get_categories()
        self.manufacturers = Manufacturer.get_manufacturers()
        self.currencies = Currency.get_currencies()
        self.primary_currency = next((currency for currency in self.currencies if currency.is_primary), None)
        
        if self.primary_currency is None:
            raise ImproperlyConfigured('No primary currency is defined for Doorsale.'
                                       ' You should defined primary currency for the system with exchange rate of 1.'
                                       ' All prices & costs should be defined in primary currency value.')
        
        if self.primary_currency.exchange_rate != 1:
            raise ImproperlyConfigured('Primary currency should have exchange rate of 1.'
                                       ' All prices & costs should be defined in primary currency value.')            
            
    def get_context_data(self, **kwargs):
        context = super(CatalogBaseView, self).get_context_data(**kwargs)
        
        # Setting data context for catalog base template
        breadcrumbs = ({ 'name': 'Home', 'url': reverse('catalog_index')},)
        if 'breadcrumbs' in context:
            breadcrumbs += context['breadcrumbs']
        
        # Getting user selected currency from session, if not defined than selecting default currency
        user_currency = self.request.session.get('user_currency', self.primary_currency.code)
        
        # If user currency is not active than choosing default currency
        user_currency = next((currency for currency in self.currencies if currency.code == user_currency), self.primary_currency)
        
        context['breadcrumbs'] = breadcrumbs    
        context['categories'] = (category for category in self.categories if category.parent is None)
        context['manufacturers'] = self.manufacturers
        context['currencies'] = self.currencies
        context['primary_currency'] = self.primary_currency
        context['user_currency'] = user_currency
        
        return context


class IndexView(CatalogBaseView):
    """
    Displays list of featured and recently added products
    """
    template_name = 'catalog/catalog_index.html'
    
    def get(self, request):
        featured_products = Product.featured_products()
        recent_products = Product.recent_products(MAX_RECENT_ARRIVALS)
        
        return super(IndexView, self).get(request,
                                          featured_products=featured_products,
                                          recent_products=recent_products)


class CategoryProductsView(CatalogBaseView):
    """
    Displays list products from the Category
    """
    template_name = 'catalog/category_products.html'
    
    def get(self, request, slug):
        category = next((category for category in self.categories if category.slug == slug), None)
        
        if category is None:
            raise Http404()
        
        breadcrumbs = category.get_breadcrumbs()
        products = Product.category_products(category)
        
        return super(CategoryProductsView, self).get(request,
                                                     category=category,
                                                     products=products,
                                                     breadcrumbs=breadcrumbs,
                                                     page_title=category.name)


class ManufacturerProductsView(CatalogBaseView):
    """
    Displays list of products from the Manufacturer
    """
    template_name = 'catalog/manufacturer_products.html'
    
    def get(self, request, slug):
        manufacturer = next((manufacturer for manufacturer in self.manufacturers if manufacturer.slug == slug), None)
        
        if manufacturer is None:
            raise Http404()
        
        breadcrumbs = manufacturer.get_breadcrumbs()
        products = Product.manufacturer_products(manufacturer)
        
        return super(ManufacturerProductsView, self).get(request,
                                                         manufacturer=manufacturer,
                                                         products=products,
                                                         breadcrumbs=breadcrumbs,
                                                         page_title=manufacturer.name)        


class SearchProductsView(CatalogBaseView):
    """
    Displays list of products from the search query
    """
    template_name = 'catalog/search_products.html'
    
    def get(self, request):
        q = request.REQUEST.get('q', None)
        
        if not q:
            return HttpResponseRedirect(reverse('catalog_index'))
        
        page_title = 'Search: ' + q
        params = { 'q': q.encode('utf-8')}
        query = '?' + urllib.urlencode(params)
        breadcrumbs = ({'name': page_title, 'url': reverse('catalog_search') + query },)
        form = AdvanceSearchForm(initial={'keyword': q})
        products = Product.search_products(q)
        return super(SearchProductsView, self).get(request,
                                                   q=q,
                                                   breadcrumbs=breadcrumbs,
                                                   form=form,
                                                   products=products,
                                                   page_title=page_title)
    
    def post(self, request):
        form = AdvanceSearchForm(request.POST)
        
        is_valid = form.is_valid()
        data = form.cleaned_data
        q=data.get('keyword', '')
        params = { 'q': q.encode('utf-8')}
        query = '?' + urllib.urlencode(params)
        breadcrumbs = ({'name': 'Search: ' + q, 'url': reverse('catalog_search') + query },)
        
        products = None
        if is_valid:
            products = Product.search_advance_products(data['keyword'], data['category'], data['manufacturer'], data['price_from'], data['price_to'], self.categories)
        
        return super(SearchProductsView, self).get(request,
                                                   q=q,
                                                   breadcrumbs=breadcrumbs,
                                                   form=form,
                                                   products=products)
    


class ProductDetailView(CatalogBaseView):
    """
    Displays product details
    """
    template_name = 'catalog/product_detail.html'
    
    def get(self, request, product_id, slug):
        try:
            product = Product.get_detail(int(product_id))
        except Product.DoesNotExist:
            raise Http404()
        
        return super(ProductDetailView, self).get(request,
                                                  product=product,
                                                  breadcrumbs=product.get_breadcrumbs(self.categories),
                                                  page_title=product.name)


class ChangeCurrencyView(View):
    """
    Change user's default currency and redirect to current page
    """
    def post(self, request):
        next_url = request.POST['next'] or reverse('catalog_index')
        user_currency = request.POST['user_currency']
        request.session['user_currency'] = user_currency
        
        return HttpResponseRedirect(next_url)
        