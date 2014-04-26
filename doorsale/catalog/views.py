from django.conf import settings
from django.http import Http404
from django.shortcuts import render

from doorsale.catalog.models import Category, Product


MAX_RECENT_ARRIVALS = getattr(settings, 'MAX_RECENT_ARRIVALS', 10)



def index(request):
    """
    Displays list of featured and recently added products
    """
    featured_products = Product.get_featured()
    recent_products = Product.get_recent(MAX_RECENT_ARRIVALS)
    return render(request, 'catalog/catalog_index.html', locals())



def category_products(request, slug):
    """
    Displays list of products in the specified category
    """
    all_categories = [category for category in Category.get_categories() if category.slug==slug]
    if len(all_categories):
        category = all_categories[0]
    else:
        raise Http404()
    
    products = Product.get_by_category(category)
    return render(request, 'catalog/category_products.html', locals())