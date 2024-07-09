from django import template
register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def range(min=2):
    return range(min)

@register.filter(name='sum')
def sum_filter(value):
    return sum(value)
