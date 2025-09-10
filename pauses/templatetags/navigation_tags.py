from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def is_practice_section(context):
    request = context["request"]
    PRACTICE_URLS = [
        "observation",
        "feelings",
        "needs",
        "update_pause",
        "update_feelings",
        "update_needs",
    ]

    return request.resolver_match and request.resolver_match.url_name in PRACTICE_URLS
