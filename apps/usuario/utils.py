#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404
from django.utils import formats
# from apps.expediente.models import *
#from apps.evento.models import *
#from apps.publicaciones.models import *


# import xhtml2pdf.pisa as pisa


#Las funciones de abajo son para validar a qué "grupo de usuario"
#pertenece el usuario que está logueado (que estás usando).

# def in_clientes_group(user):
# 	av_groups = user.groups.all()
# 	for group in av_groups:
# 		if 'Clientes' in str(group):
# 			return True
# 	return False
#
# def in_productos_group(user):
# 	av_groups = user.groups.all()
# 	for group in av_groups:
# 		if 'Productos' in str(group):
# 			return True
# 	return False
# ---------------------------------------------------------------------------
def is_granted(user, role):
    if user.is_superuser:
        return True

    if role == 'ROLE_ADMIN':
        role = 'Administrador'

    if role == 'ROLE_RESPONSABLE':
        role = 'Responsable'

    if role == 'ROLE_DOCTORANDO':
        role = 'Doctorando'

    if role == 'ROLE_ESPECIALISTA':
        role = 'Especialista'

    if role == 'ROLE_TUTOR':
        role = 'Tutor'

    for x in user.groups.all():
        if x.name == role:
            return True

    return False
# ---------------------------------------------------------------------------
def is_authenticatedas(user, role):
    if user.is_superuser:
        return False

    if role == 'ROLE_ADMIN':
        role = 'Administrador'

    if role == 'ROLE_RESPONSABLE':
        role = 'Responsable'

    if role == 'ROLE_DOCTORANDO':
        role = 'Doctorando'

    if role == 'ROLE_ESPECIALISTA':
        role = 'Especialista'


    for x in user.groups.all():
        if x.name == role:
            return True

    return False
# ---------------------------------------------------------------------------
def get_month_name(month):
    if month == 1: return 'Enero'
    if month == 2: return 'Febrero'
    if month == 3: return 'Marzo'
    if month == 4: return 'Abril'
    if month == 5: return 'Mayo'
    if month == 6: return 'Junio'
    if month == 7: return 'Julio'
    if month == 8: return 'Agosto'
    if month == 9: return 'Septiembre'
    if month == 10: return 'Octubre'
    if month == 11: return 'Noviembre'
    if month == 12: return 'Diciembre'

    return ''
# ---------------------------------------------------------------------------
def get_natural_date(date):
    day = formats.date_format(date, "d")
    month = int(formats.date_format(date, "m"))
    month = get_month_name(month)
    year = formats.date_format(date, "Y")

    return day + ' de ' + month + ' de ' + year
# ---------------------------------------------------------------------------
def get_natural_month_year(date):
    month = int(formats.date_format(date, "m"))
    year = formats.date_format(date, "Y")
    month_nemo = ''

    if month == 1: month_nemo = 'Ene.'
    if month == 2: month_nemo = 'Feb.'
    if month == 3: month_nemo = 'Mar.'
    if month == 4: month_nemo = 'Abr.'
    if month == 5: month_nemo = 'May.'
    if month == 6: month_nemo = 'Jun.'
    if month == 7: month_nemo = 'Jul.'
    if month == 8: month_nemo = 'Ago.'
    if month == 9: month_nemo = 'Sep.'
    if month == 10: month_nemo = 'Oct.'
    if month == 11: month_nemo = 'Nov.'
    if month == 12: month_nemo = 'Dic.'

    return month_nemo + ' ' + str(year)
# ---------------------------------------------------------------------------
