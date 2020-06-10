# -*- coding: utf-8 -*-
#from apps.expediente.models import EspecialidadDoctorado
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
#from apps.expediente.models import *
from apps.expediente.models import *


from django.db import models


# Create your models here.
# ---------------------------------------------------------------------------------------



# class Tesis(models.Model):
#     history = AuditlogHistoryField()
#     especialidad_doctorado = models.OneToOneField(EspecialidadDoctorado, on_delete=models.CASCADE, null=False, blank=False, default='')
#
#     titulo_tesis=models.CharField(max_length=255, null=False, blank=False, unique=True)
#     archivo = models.FileField(upload_to="tesis/", null=True, blank=True)
#     created_at = models.DateTimeField("Fecha de Creado", auto_now_add=True, default='')
#     updated_at = models.DateTimeField("Fecha de actualización", auto_now=True, auto_now_add=False)
#
#     class Meta:
#         db_table = 'tesis'
#         verbose_name = 'Tesis'
#         verbose_name_plural = 'Tesis'
#         ordering = ['-titulo_tesis']
#
# auditlog.register(Tesis)
# ---------------------------------------------------------------------------------------