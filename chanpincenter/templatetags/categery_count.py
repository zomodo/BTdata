from django import template
from chanpincenter import models
register=template.Library()

@register.filter(name='resources_count')
def category_count(value):
    c=models.Resource.objects.filter(category_id=value).count()
    return c

@register.filter(name='share_example_count')
def category_count(value):
    c=models.ShareExample.objects.filter(category_id=value).count()
    return c