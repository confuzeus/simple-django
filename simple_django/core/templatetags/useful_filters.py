from django import template

register = template.Library()


@register.filter()
def is_number(value):

    if not isinstance(value, bool):
        if isinstance(value, int):
            return True
        elif isinstance(value, float):
            return True

    return False


@register.filter()
def is_string(value):
    if isinstance(value, str):
        return True
    else:
        return False
