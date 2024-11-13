from django import template


register = template.Library()


@register.filter
def filter_comments(value, arg):
    sub_comment = value.filter(parent_id=arg)
    return sub_comment.select_related('parent')
