from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View

from doorstep.views import BaseView
from doorstep.catalog.forms import AdvancedSearchForm
from doorstep.catalog.models import Manufacturer, Category, Product
from doorstep.financial.models import Currency


class CatalogBaseView(BaseView):
    """
    Generic view for all catalog pages
    """
    style_name = 'catalog'
    catalog_template_name = 'catalog/catalog_base.html'

    def __init__(self, *args, **kwargs):
        super(CatalogBaseView, self).__init__(*args, **kwargs)
        # Loading categories
        self.categories = Category.get_categories()
        self.manufacturers = Manufacturer.get_manufacturers()
        self.currencies = Currency.get_currencies()
        self.primary_currency = next(
            (currency for currency in self.currencies if currency.is_primary), None)

        if self.primary_currency is None:
            raise ImproperlyConfigured('No primary currency is defined for Doorstep.'
                                       ' You should defined primary currency for the system with exchange rate of 1.'
                                       ' All prices & costs should be defined in primary currency value.')

        if self.primary_currency.exchange_rate != 1:
            raise ImproperlyConfigured('Primary currency should have exchange rate of 1.'
                                       ' All prices & costs should be defined in primary currency value.')

    def get_context_data(self, **kwargs):
        context = super(CatalogBaseView, self).get_context_data(**kwargs)

        # Setting data context for catalog base template
        breadcrumbs = ({'name': 'All', 'url': reverse('catalog_index')},)
        if 'breadcrumbs' in context:
            breadcrumbs += context['breadcrumbs']

        # Getting user selected currency from session, if not defined than
        # selecting default currency
        default_currency = self.request.session.get('default_currency', self.primary_currency.code)

        # If user currency is not active than choosing primary currency
        default_currency = next(
            (currency for currency in self.currencies if currency.code == default_currency), self.primary_currency)

        context['breadcrumbs'] = breadcrumbs
        context['categories'] = [category for category in self.categories if category.parent is None]
        context['manufacturers'] = self.manufacturers
        context['currencies'] = self.currencies
        context['primary_currency'] = self.primary_currency
        context['default_currency'] = default_currency
        context['catalog_template_name'] = self.catalog_template_name

        return context

    @classmethod
    def get_page_size(cls):
        """
        Returns page size for products listing
        """
        return int(cls.get_config('PAGE_SIZE'))


class IndexView(CatalogBaseView):
    """
    Displays list of featured and recently added products
    """
    template_name = 'catalog/catalog_index.html'

    def get(self, request):
        featured_products = Product.featured_products()
        recent_products = Product.recent_products(self.get_max_recent_arrivals())

        return super(IndexView, self).get(request,
                                          featured_products=featured_products,
                                          recent_products=recent_products)

    @classmethod
    def get_max_recent_arrivals(cls):
        return int(cls.get_config('MAX_RECENT_ARRIVALS'))


class CategoryProductsView(CatalogBaseView):
    """
    Displays list products from the Category
    """
    template_name = 'catalog/category_products.html'

    def get(self, request, slug, page_num):
        category = next((category for category in self.categories if category.slug == slug), None)

        if category is None:
            raise Http404()

        breadcrumbs = category.get_breadcrumbs()
        products = paginate(Product.category_products(category), self.get_page_size(),
                            page_num, 'catalog_category', [slug])

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

    def get(self, request, slug, page_num):
        manufacturer = next(
            (manufacturer for manufacturer in self.manufacturers if manufacturer.slug == slug), None)

        if manufacturer is None:
            raise Http404()

        breadcrumbs = manufacturer.get_breadcrumbs()
        products = paginate(Product.manufacturer_products(manufacturer), self.get_page_size(),
                            page_num, 'catalog_manufacturer', [slug])

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

    def get(self, request, page_num):
        form = AdvancedSearchForm(request.GET)
        query = '?' + request.GET.urlencode()
        products = None
        category = None
        breadcrumbs = ()
        keyword = request.GET.get('keyword', None)

        if form.is_valid():
            data = form.cleaned_data
            category = data['category']
            products = paginate(Product.search_advance_products(
                data['keyword'], data['category'], data['manufacturer'],
                data['price_from'], data['price_to'], self.categories),
                self.get_page_size(), page_num, 'catalog_search', qs=query)

            if category:
                breadcrumbs = category.get_breadcrumbs()

        page_title = keyword or (category and category.name) or 'All Products'
        return super(SearchProductsView, self).get(request,
                                                   form=form,
                                                   keyword=keyword,
                                                   category=category,
                                                   products=products,
                                                   page_title=page_title,
                                                   breadcrumbs=breadcrumbs)


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
                                                  breadcrumbs=product.get_breadcrumbs(
                                                      self.categories),
                                                  page_title=product.name)


class ChangeCurrencyView(View):
    """
    Change user's default currency and redirect to current page
    """

    def post(self, request):
        next_url = request.POST['next'] or reverse('catalog_index')
        default_currency = request.POST['default_currency']
        request.session['default_currency'] = default_currency

        return HttpResponseRedirect(next_url)


def get_default_currency(request):
    if 'default_currency' in request.session:
        try:
            return Currency.objects.get(code=request.session['default_currency'])
        except Currency.DoesNotExist:
            return Currency.get_primary()

    return Currency.get_primary()


def paginate(query_set, page_size, page_num, url_name, url_args=[], qs=None):
    paginator = Paginator(query_set, page_size)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Generating paginated previous and next urls
    # if page 1 than suppressing page number in url
    if page.has_previous():
        previous_page_num = page.previous_page_number()
        if previous_page_num == 1:
            page.previous_url = reverse(url_name, args=url_args) + (qs or '')
        else:
            page.previous_url = reverse(url_name, args=(url_args + [previous_page_num])) + (qs or '')

    if page.has_next():
        next_page_num = page.next_page_number()
        page.next_url = reverse(url_name, args=(url_args + [next_page_num])) + (qs or '')

    page.page_urls = [(page_num, reverse(url_name, args=(url_args + [page_num])) + (qs or '')) for page_num in range(1, paginator.num_pages + 1)]

    return page
