from django import template
from peixuncenter import models
register=template.Library()

@register.filter(name='share_count')
def category_count(value):
    c=models.ShareFile.objects.filter(category_id=value).count()
    return c