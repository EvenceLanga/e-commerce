from django import template

register = template.Library()

@register.filter
def get(d, key):
    """Get value from dict by key."""
    return d.get(key, "")
