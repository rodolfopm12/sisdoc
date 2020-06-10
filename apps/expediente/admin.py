#-*- coding: utf-8 -*-

from django.contrib import admin
from apps.expediente.models import *
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from django.forms.utils import ErrorList

# Register your models here.
class ExpedienteResource(resources.ModelResource):
    class Meta:
        model: Expediente


#Búsquedas
class Expediente_Admin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('numero_expediente', 'numero_acuerdo', 'created_at', 'updated_at', 'estado')
    search_fields = ('numero_expediente', 'numero_acuerdo', 'created_at', 'updated_at')
    #Filtros
    list_filter = ('created_at', 'updated_at',)
    date_hierarchy = "created_at"

    resource_class = ExpedienteResource

admin.site.register(Expediente, Expediente_Admin)
# ---------------------------------------------------------------------------------------
class CategoriadocenteAdmin(admin.ModelAdmin):
    list_display = ('categoria_docente',)

admin.site.register(Categoria_docente, CategoriadocenteAdmin)
# ---------------------------------------------------------------------------------------
class CategoriainvestigativaAdmin(admin.ModelAdmin):
    list_display = ('categoria_investigador',)

admin.site.register(Categoria_investigador, CategoriainvestigativaAdmin)
# ---------------------------------------------------------------------------------------
class GradocientificoAdmin(admin.ModelAdmin):
    list_display = ('grado_cientifico',)

admin.site.register(Grado_cientifico, GradocientificoAdmin)
# ---------------------------------------------------------------------------------------
class ProfesionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

admin.site.register(Profesion, ProfesionAdmin)
# ---------------------------------------------------------------------------------------
class ContinenteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

    list_filter = ('nombre',)
admin.site.register(Continente, ContinenteAdmin)
# ---------------------------------------------------------------------------------------
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

    list_filter = ('nombre',)
admin.site.register(Pais, PaisAdmin)
# ---------------------------------------------------------------------------------------
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

admin.site.register(Provincia, EstadoAdmin)
# ---------------------------------------------------------------------------------------
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

admin.site.register(Municipio, MunicipioAdmin)
# ---------------------------------------------------------------------------------------
class DoctorandoResource(resources.ModelResource):
    class Meta:
        model: Doctorando


class Doctorando_Admin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('ci', 'pasaporte', 'telefono_fijo', 'movil', 'edad', 'estado_civil',)
    search_fields = ("ci",)

admin.site.register(Doctorando, Doctorando_Admin)
# ---------------------------------------------------------------------------------------