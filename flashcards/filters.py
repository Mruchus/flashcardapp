from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def capitalize(value):
    return [v.capitalize() for v in value]