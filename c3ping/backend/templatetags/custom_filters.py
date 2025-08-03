from django import template

register = template.Library()

@register.filter
def split_by_comma(value):
    if not value:
        return []
    return [item.strip() for item in value.split(',')]
