from django import template
from django.utils.http import urlencode


register = template.Library()


@register.simple_tag(takes_context=True)
def add_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    url = urlencode(query)
    result = url[::-1].replace('/', '', 1)[::-1]
    return result
