from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight_second_letter(word, css_class="text-otherpink"):
    if len(word) < 2:
        return word
    first = word[0]
    second = word[1]
    rest = word[2:]
    return mark_safe(f'{first}<span class="{css_class}">{second}</span>{rest}')
