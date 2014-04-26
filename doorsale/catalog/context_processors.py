from .models import Category


def bootstrip(request):
    """
    Preload categories
    """
    return { 'categories': Category.get_nested_categories() }