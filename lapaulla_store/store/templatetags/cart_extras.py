from django import template

register = template.Library()

# Your custom filters or tags will go here
# For example, if you have a filter named 'multiply':
@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''