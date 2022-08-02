from django import template

from information.models import TerminosCondiciones
register = template.Library()


@register.simple_tag
def get_terms_conds():
    return TerminosCondiciones.objects.first()
