from django import template

register = template.Library()


@register.filter
def label_title(value):
    """'< 50,000 KES (~$400) - Scoped feature' -> '< 50,000 KES (~$400)'"""
    return str(value).split(' \u2014 ')[0]


@register.filter
def label_sub(value):
    """'< 50,000 KES (~$400) - Scoped feature' -> 'Scoped feature' ('' if there is none)"""
    parts = str(value).split(' \u2014 ', 1)
    return parts[1] if len(parts) > 1 else ''
