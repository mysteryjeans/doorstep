from django.shortcuts import render

from doorsale.catalog.models import Category

def index(request):
    
    categories = Category.get_nested_categories()
    return render(request, 'catalog/catalog_index.html', locals())