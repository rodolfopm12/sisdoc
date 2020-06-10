#-*- coding: utf-8 -*-
from django import template

from apps.usuario.utils import *

register = template.Library()
# ---------------------------------------------------------------------------
@register.filter(name='has_role')
def has_role(user, role):
    return is_granted(user, role)
# ---------------------------------------------------------------------------
