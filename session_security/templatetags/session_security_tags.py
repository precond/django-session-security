from django import template

from session_security.settings import WARN_AFTER, EXPIRE_AFTER, WARN_LOCK

register = template.Library()


@register.filter
def expire_after(request):
    return EXPIRE_AFTER


@register.filter
def warn_after(request):
    return WARN_AFTER


@register.filter
def warn_lock(request):
    # Return Javascript boolean value instead of Python value
    if WARN_LOCK:
        return 'true'
    else:
        return 'false'
