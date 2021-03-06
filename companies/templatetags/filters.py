from django import template

register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


# noinspection PyShadowingBuiltins
@register.filter
def iter(gen):
    try:
        return next(gen)
    except StopIteration:
        return 'Completed Iteration'


@register.filter
def exists(choice):
    for field in choice:
        return field
    return False
