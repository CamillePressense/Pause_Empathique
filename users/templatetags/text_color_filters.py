from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight_second_letter(value, css_class='text-otherpink'):
    if len(value) < 2:
        return value
    first = value[0]
    second = value[1]
    rest = value[2:]
    return mark_safe(f'{first}<span class="{css_class}">{second}</span>{rest}')