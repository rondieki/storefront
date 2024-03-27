from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    if css_classes:
        css_classes += f' {arg}'
    else:
        css_classes = arg
    return value.as_widget(attrs={'class': css_classes})

@register.filter
def replace_string(value, old, new):
    """Custom template filter to replace a substring in a string."""
    return value.replace(old, new)
