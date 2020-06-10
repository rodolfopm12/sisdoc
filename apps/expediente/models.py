#-*- coding: utf-8 -*-
from django.db import models
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
import datetime
from django.forms import model_to_dict
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import post_save

# Create your models here.
from apps import usuario
from apps.usuario.models import UserProfile
from config import settings

# STATUS_CHOICES = (
#     (0, "Pendiente"),
#     (1, "Aprovado"),
#     (2, "Eliminado"),
# )

ESTADOCIVIL_CHOICES = (
    (0, "Casado"),
    (1, "Divorciado"),
    (2, "Viudo"),
)

GRADO_CIENTIFICO_CHOICES = (
    (0, "Master en Ciencias"),
    (1, "Doctor en Ciencias"),
)


# ---------------------------------------------------------------------------------------
class Expediente(models.Model):
    history = AuditlogHistoryField()
    numero_expediente=models.IntegerField(verbose_name="Número del Expediente", blank=False, null=False, unique=True)
    numero_acuerdo=models.IntegerField(blank=False, null=False, unique=True)
    #fecha_matriculacion=models.DateField("fecha", auto_now= True, auto_now_add= False)
    created_at = models.DateTimeField("Fecha de Creado", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now=True, auto_now_add= False)
    estado = models.BooleanField(default=True, null=False, blank=False)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'expediente'
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'
        ordering = ['-created_at']
# ---------------------------------------------------------------------------------------
class Profesion(models.Model):
    history = AuditlogHistoryField()
    nombre=models.CharField(max_length=100, blank=False, unique=True)
    #ano_graduado=models.PositiveIntegerField(u"Año de graduación", null=True, blank=True)

    class Meta:
        db_table = 'profesion'
        verbose_name = "Profesión"
        verbose_name_plural = "Profesiones"
        ordering = ['-nombre']

    def __str__(self):
        return self.nombre
# ---------------------------------------------------------------------------------------
class Especialidad(models.Model):
    especialidades=models.CharField("Especialidades", max_length=100)

    class Meta:
        db_table = 'especialidades'
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['-especialidades']

    def __str__(self):
        return self.especialidades
# ---------------------------------------------------------------------------------------
class Categoria_docente(models.Model):
    history = AuditlogHistoryField()
    categoria_docente = models.CharField("Categoría Docente", max_length=70, unique=True)

    def __str__(self):
        return self.categoria_docente

    class Meta:
        db_table = 'categoria_docente'
        verbose_name = "Categoría Docente"
        verbose_name_plural = "Categorías Docentes"
        ordering = ['-categoria_docente']
auditlog.register(Categoria_docente)
# ---------------------------------------------------------------------------------------
class Categoria_especial(models.Model):
    history = AuditlogHistoryField()
    categoria_especial = models.CharField("Categoría Especial", max_length=70, unique=True)

    def __unicode__(self):
        return self.categoria_especial

    def __str__(self):
        return self.categoria_especial

    class Meta:
        db_table = 'categoria_especial'
        verbose_name = "Categoría Especial"
        verbose_name_plural = "Categorías Especiales"
        ordering = ['-categoria_especial']
auditlog.register(Categoria_especial)
# ---------------------------------------------------------------------------------------
class Grado_cientifico(models.Model):
    history = AuditlogHistoryField()
    grado_cientifico = models.CharField(max_length=70, unique=True)

    class Meta:
        db_table = 'grado_cientifico'
        verbose_name = "Grado Científico"
        verbose_name_plural = "Grados_científicos"
        ordering = ['-grado_cientifico']

    def __str__(self):
        return self.grado_cientifico

auditlog.register(Grado_cientifico)
# ---------------------------------------------------------------------------------------
class Categoria_investigador(models.Model):
    categoria_investigador = models.CharField(max_length=70, unique=True)

    class Meta:
        db_table = 'categoria_investigador'
        verbose_name = "Categoría de Investigador"
        verbose_name_plural = "Categorías de Investigadores"
        ordering = ['categoria_investigador']

    def __str__(self):
        return self.categoria_investigador
# ---------------------------------------------------------------------------------------
class Continente(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'continente'
        verbose_name = 'Continente'
        verbose_name_plural = 'Continentes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
# ---------------------------------------------------------------------------------------
class Pais(models.Model):
    continente = models.ForeignKey(Continente, on_delete=models.CASCADE, null=False, blank=False)
    nombre = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        db_table = 'pais'
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
# ---------------------------------------------------------------------------------------
class Provincia(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=False, blank=False)
    nombre = models.CharField(max_length=150, null=False, blank=False)


    class Meta:
        db_table = 'provincia'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
# ---------------------------------------------------------------------------------------
class Municipio(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'municipio'
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
# ---------------------------------------------------------------------------------------
class Organismo(models.Model):
    nombre_organismo = models.CharField(max_length=255, null=False, blank=False)
    cod_organismo = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'organismo'
        verbose_name = 'Organismo'
        verbose_name_plural = 'Organismos'
        ordering = ['-nombre_organismo']

    def __str__(self):
        return self.nombre_organismo
# ---------------------------------------------------------------------------------------
class CentroTrabajo(models.Model):
    nombre_trabajo = models.CharField(max_length=255, null=False, blank=False)
    direccion_trabajo = models.CharField(u"Dirección del centro", max_length=200, null=True, blank=True)
    cargo_ocupa = models.CharField(max_length=255, null=False, blank=False)
    telefono_trabajo = models.CharField(max_length=20, verbose_name="Teléfono Trabajo", null=True, blank=True)
    email_trabajo = models.EmailField(blank=True, verbose_name="Email trabajo", null=True)

    class Meta:
        db_table = 'centro_trabajo'
        verbose_name = 'Datos de centro de trabajo'
        verbose_name_plural = 'Datos de centros de trabajos'
        ordering = ['-nombre_trabajo']
# ---------------------------------------------------------------------------------------
class EspecialidadDoctorado(models.Model):
    nombre_especialidaddoc = models.CharField(max_length=255, null=True, blank=True, unique=True)

    class Meta:
        db_table = 'especialidad_doctorado'
        verbose_name = 'Especialidad de Doctorado'
        verbose_name_plural = 'Especialidades de Doctorados'
        ordering = ['-nombre_especialidaddoc']

    def __str__(self):
        return self.nombre_especialidaddoc
# ---------------------------------------------------------------------------------------
class Tesis(models.Model):
    history = AuditlogHistoryField()
    especialidad_doctorado = models.OneToOneField(EspecialidadDoctorado, on_delete=models.CASCADE, null=True, blank=True, default='')
    titulo_tesis = models.CharField(max_length=255, null=False, blank=False, unique=True)
    archivo = models.FileField(upload_to="tesis/", null=True, blank=True)
    created_at = models.DateTimeField("Fecha de Creado", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now=True, auto_now_add=False)

    class Meta:
        db_table = 'tesis'
        verbose_name = 'Tesis'
        verbose_name_plural = 'Tesis'
        ordering = ['-titulo_tesis']

    def __str__(self):
        return self.titulo_tesis

auditlog.register(Tesis)
# ---------------------------------------------------------------------------------------
class Tutor(models.Model):
    history = AuditlogHistoryField()
    nombre_tutor = models.CharField(max_length=50, null=False, blank=False, verbose_name="Nombre del Tutor")
    apellidos_tutor = models.CharField(max_length=50,null=False, blank=False, default='')
    #segundo_apellidos_tutor = models.CharField(max_length=50, blank=False, unique=True, verbose_name="Segundo Apellido")
    email_tutor = models.EmailField(blank=True, verbose_name="Emails")
    telefono_tutor = models.CharField(max_length=20, verbose_name="Teléfono", default='')

    categoria_docente = models.ForeignKey(Categoria_docente, on_delete=models.CASCADE, null=False, blank=False, default='')
    categoria_especial = models.ForeignKey(Categoria_especial, on_delete=models.CASCADE, null=True, blank=False, default='')
    grado_cientifico = models.ForeignKey(Grado_cientifico, on_delete=models.CASCADE, null=False, blank=False, default='')
    categoria_investigador = models.ForeignKey(Categoria_investigador, on_delete=models.CASCADE, null=False, blank=False, default='')
    organismo = models.ForeignKey(Organismo, on_delete=models.CASCADE, null=True, blank=False)
    centro_trabajo = models.ForeignKey(CentroTrabajo, on_delete=models.CASCADE, null=True, blank=False)

    tesis = models.ManyToManyField(Tesis, related_name='Tesis')

    class Meta:
        db_table = 'tutor'
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutores'
        ordering = ['-nombre_tutor']
auditlog.register(Tutor)
# ---------------------------------------------------------------------------------------
class Doctorando(models.Model):
    history = AuditlogHistoryField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.CASCADE,  default='')
    expediente = models.OneToOneField(Expediente, on_delete=models.CASCADE, null=False, blank=False)

    ci = models.CharField(u"Número de Carné de Identidad", max_length=11, db_index=True, null=True, blank=True, unique=True)
    pasaporte = models.CharField(u"Número de Pasaporte", max_length=20, db_index=True, null=True, blank=True, unique=True)
    direccion = models.CharField(u"Dirección", max_length=200, null=True, blank=True)
    telefono_fijo = models.CharField(max_length=20, verbose_name="Teléfono", null=True, blank=True)
    movil = models.CharField(u"Número de Móvil", max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", null=True, blank=False)
    edad = models.PositiveIntegerField("edad")
    estado_civil = models.IntegerField(choices=ESTADOCIVIL_CHOICES)

    profesion = models.ForeignKey(Profesion, on_delete=models.CASCADE, null=False, blank=False)
    categoria_docente = models.ForeignKey(Categoria_docente, on_delete=models.CASCADE, null=True, blank=True)
    categoria_especial = models.ForeignKey(Categoria_especial, on_delete=models.CASCADE, null=True, blank=False)
    grado_cientifico = models.ForeignKey(Grado_cientifico, on_delete=models.CASCADE, null=True, blank=True)
    categoria_investigador = models.ForeignKey(Categoria_investigador, on_delete=models.CASCADE, null=False,
                                               blank=False)
    continente = models.ForeignKey(Continente, on_delete=models.SET_NULL, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, blank=True, null=True)
    organismo = models.ForeignKey(Organismo, on_delete=models.CASCADE, null=True, blank=False)
    centro_trabajo = models.ForeignKey(CentroTrabajo, on_delete=models.CASCADE, null=True, blank=False)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, default='')
    tesis = models.OneToOneField(Tesis, on_delete=models.CASCADE, null=False, blank=False, default='')



    def edad(self):
        result = 0
        if self.fecha_nacimiento:
            return (datetime.date.today() - self.fecha_nacimiento).days / 365

    # def calculate_edad(fecha_nacimiento):
    #     today = date.today()
    #     return today.year - fecha_nacimiento.year -((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

    class Meta:
        db_table = "doctorando"
        verbose_name = 'Doctorando'
        verbose_name_plural = 'Doctorandos'
        ordering = ['-ci']

#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#       Docotrando.objects.create(user=instance)
       #UserProfile.objects.create(user=instance)
#post_save.connect(create_user_profile, sender=User)

auditlog.register(Doctorando)
# ---------------------------------------------------------------------------------------