from django import template

register=template.Library()

@register.filter(name='div')
def div(value):
    p=round(value/10000,2)
    return p
