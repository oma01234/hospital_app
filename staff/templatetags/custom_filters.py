from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """ Custom filter to access dictionary items """
    return dictionary.get(key)
