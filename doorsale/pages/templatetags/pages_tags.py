from django import template

from doorsale.pages.models import Link, FlatPage


register = template.Library()


@register.inclusion_tag('pages/pages_links.html')
def get_pages_links():
    """
    Returns pages links
    """
    groups = []
    links = [link for link in Link.objects.order_by('group', 'id').all().prefetch_related('page') if link.page is None or link.page.is_active]
    
    for link in links:
        if not link.group in groups:
            groups.append(link.group)
    
    groups = [{
        'name': group,
        'links': [{
            'name': link.name,
            'url': link.page.get_absolute_url() if link.page else link.url
            } for link in links if link.group == group
        ]} for group in groups]
   
    return {'groups': groups }