from django import template

register = template.Library()

@register.filter(name='split_space')
def split_space(value):
    return value.split(' ')
