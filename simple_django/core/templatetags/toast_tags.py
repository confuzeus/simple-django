from django import template

register = template.Library()


@register.simple_tag
def get_toast_color_scheme(toast_tag):
    if toast_tag == "info":
        return "text-bg-info"
    elif toast_tag == "success":
        return "text-bg-success"
    elif toast_tag == "warning":
        return "text-bg-warning"
    elif toast_tag == "danger":
        return "text-bg-danger"
    return ""


@register.simple_tag
def get_toast_close_button_color(toast_tag):
    if toast_tag == "info":
        return "btn-close-dark"
    elif toast_tag == "success":
        return "btn-close-white"
    elif toast_tag == "warning":
        return "btn-close-dark"
    elif toast_tag == "danger":
        return "btn-close-white"
    return ""
