from django import template
register = template.Library()


@register.filter(name='lookup')
def lookup(value, num, default=""):
    if num in value:
        return value[num]
    else:
        return default