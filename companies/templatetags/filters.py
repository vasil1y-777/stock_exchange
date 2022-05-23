from django import template

register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def iter(gen):
    try:
        return next(gen)
    except StopIteration:
        return 'Completed Iteration'