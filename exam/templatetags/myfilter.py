from django import template

register = template.Library()

@register.filter(name='get')
def get(alist, index):
    return alist[index]