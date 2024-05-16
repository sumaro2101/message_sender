from django import template
from users.models import NavBarList, Sublist
from django.utils.http import urlencode

register = template.Library()

@register.inclusion_tag('includes/nav_bar.html', takes_context=True)
def nav_bar_tag(context, catg_selected=1):
    nav_items = NavBarList.objects.all()
    sub_nav_items = Sublist.objects.all()
    
    return {
        'nav_items': nav_items,
        'catg_selected': catg_selected,
        'sub_nav_items': sub_nav_items,
        'is_staff': context.request.user.is_staff
    }

@register.simple_tag(takes_context=True)
def add_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
