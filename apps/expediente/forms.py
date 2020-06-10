# -*- coding: utf-8 -*-
# from django import forms
# from django.forms.extras.widgets import SelectDateWidget
# from django.utils import timezone
# -----------------
from django.forms import *
# from django.forms.utils import ErrorList


from .models import *
from apps.usuario.models import *

# from apps.expediente.models import Expediente

BOOLEAN_CHOICES = (('1', 'Activo'), ('0', 'Pasivo'))


class ExpedienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['numero_acuerdo'].widget.attrs['autofocus'] = True
        self.fields['estado'].widget.attrs['class'] = 'checkbox icheck'

    class Meta:
        model = Expediente
        fields = ['numero_acuerdo', 'numero_expediente', 'estado']
        labels = {
            'numero_expediente': 'Número de Expediente',
            'numero_acuerdo': 'Número de acuerdo',
            'estado': 'Estado del expediente (Activo)',
        }
        widgets = {
            'numero_acuerdo': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el número de acuerdo',
                }
            ),
            'numero_expediente': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el número de expediente',
                }
            ),
            'estado': CheckboxInput(
                attrs={
                    'checked': True,
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# ------------------------------------------------------------------------------
class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

    """User form."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'image']
        # exclude = ['username']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo',
            'image': 'Foto para el Expediente',
        }
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Nombre del Doctorando',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Apellidose del Doctorando',
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Correo Electrónico',
                }
            ),
            'image': FileInput(
                attrs={
                    'placeholder': 'Foto para el Expediente',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# ------------------------------------------------------------------------------
class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['sexo'].required = True

    class Meta:
        model = UserProfile
        fields = ['sexo', 'nota']
        exclude = ['user']
        labels = {
            'sexo': 'Sexo',
            'nota': 'Nota',
        }
        widgets = {
            # 'sexo': ModelChoiceField(
            #     attrs={
            #         'placeholder': 'Sexo',
            #     }
            # ),
            'nota': Textarea(
                attrs={
                    'rows': '3',
                    'placeholder': 'Nota'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# ------------------------------------------------------------------------------
class DoctorandoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['pais'].queryset = Pais.objects.none()
        self.fields['provincia'].queryset = Provincia.objects.none()
        self.fields['municipio'].queryset = Municipio.objects.none()
        self.fields['fecha_nacimiento'].widget.attrs = {'class': 'date-picker form-control'}
        # self.fields['profesion'].widget.attrs = {'class':'form-control select2', 'placeholder': 'Escoger', 'required': True, 'a', }

        # self.fields['ci'].widget.attrs = {'placeholder': 'Carnet de Identidad', }
        # self.fields['pasaporte'].widget.attrs = {'placeholder': 'Pasaporte', }
        # self.fields['direccion'].required = True
        # self.fields['direccion'].widget.attrs = {'placeholder': 'Dirección'}
        # self.fields['telefono_fijo'].widget.attrs = {'placeholder': 'Teléfono'}
        # self.fields['movil'].widget.attrs = {'placeholder': 'Móvil'}
        #
        # self.fields['estado_civil'].required = True

        # self.fields['grado_cientifico'].widget.label = u"Categoría Científica"
        # self.fields['continente'].required = True
        # self.fields['pais'].required = True
        # self.fields['provincia'].widget.label = u"Estado o Provincia"
        # self.fields['provincia'].required = True

    class Meta:
        model = Doctorando
        fields = ['ci', 'pasaporte', 'direccion', 'telefono_fijo', 'movil', 'fecha_nacimiento', 'continente', 'pais',
                  'provincia', 'municipio', 'categoria_docente', 'estado_civil', 'profesion', 'grado_cientifico',
                  'organismo', 'centro_trabajo']  # '__all__'
        exclude = ['expediente', 'user', 'tesis']
        labels = {
            'ci': 'Número de Carnet de Identidad',
            'pasaporte': 'Pasaporte',
            'direccion': 'Dirección',
            'telefono_fijo': 'Número de Teléfono fijo',
            'movil': 'Número de Móvil',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'continente': 'Continente',
            'pais': 'País',
            'provincia': 'Estado o Provincia',
            'municipio': 'Municipio',
            'categoria_docente': 'Categoría Docente',
            'estado_civil': 'Estado Civil',
            'profesion': 'Graduado Universitario de:',
            'grado_cientifico': 'Categoría Científica',
            'organismo': 'Organismo',
        }

        # widgets = {
        #     'profesion': Select(
        #         attrs={
        #             'class': 'form-control select2',
        #             'placeholder': 'Escoger Profesión',
        #             'required': True,
        #             'allowClear': True,
        #             'language': 'es',
        #         }
        #     ),
        # }


# ------------------------------------------------------------------------------
class CategoriaInvestigadorForm(ModelForm):
    class Meta:
        model = Categoria_investigador
        fields = ['categoria_investigador']

    def __init__(self, *args, **kwargs):
        super(CategoriaInvestigadorForm, self).__init__(*args, **kwargs)
        self.fields['categoria_investigador'].widget.label = u"Categoría de Investigador"
        self.fields['categoria_investigador'].widget.attrs = {'class': 'form-control'}


# ------------------------------------------------------------------------------
class EspecialidadForm(ModelForm):
    class Meta:
        model = Especialidad
        fields = ['especialidades']

    def __init__(self, *args, **kwargs):
        super(EspecialidadForm, self).__init__(*args, **kwargs)
        self.fields['especialidades'].widget.label = u"Especialidades"
        self.fields['especialidades'].widget.attrs = {'class': 'form-control'}


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
class CentroTrabajoForm(ModelForm):
    class Meta:
        model = CentroTrabajo
        fields = ['nombre_trabajo', 'direccion_trabajo', 'cargo_ocupa', 'telefono_trabajo', 'email_trabajo']

    def __init__(self, *args, **kwargs):
        super(CentroTrabajoForm, self).__init__(*args, **kwargs)
        self.fields['nombre_trabajo'].widget.label = u"Nombre del Centro de Trabajo"
        self.fields['nombre_trabajo'].widget.attrs = {'class': 'form-control',
                                                      'placeholder': 'Nombre del Centro de Trabajo'}
        self.fields['direccion_trabajo'].widget.label = u"Dirección del Centro"
        self.fields['direccion_trabajo'].widget.attrs = {'class': 'form-control', 'placeholder': 'Dirección del Centro'}
        self.fields['cargo_ocupa'].widget.label = u"Cargo"
        self.fields['cargo_ocupa'].widget.attrs = {'class': 'form-control', 'placeholder': 'Cargo'}
        self.fields['telefono_trabajo'].widget.label = u"Teléfono del Trabajo"
        self.fields['telefono_trabajo'].widget.attrs = {'class': 'form-control', 'placeholder': 'Teléfono del Trabajo'}
        self.fields['email_trabajo'].widget.label = u"Correo del Trabajo"
        self.fields['email_trabajo'].widget.attrs = {'class': 'form-control', 'placeholder': 'Correo del Trabajo'}


# ------------------------------------------------------------------------------
class TesisForm(ModelForm):
    class Meta:
        model = Tesis
        fields = ['titulo_tesis', 'especialidad_doctorado']
        exclude = ['archivo']

    def __init__(self, *args, **kwargs):
        super(TesisForm, self).__init__(*args, **kwargs)
        self.fields['titulo_tesis'].widget.label = u"Título de la Tesis"
        self.fields['titulo_tesis'].widget.attrs = {'class': 'form-control'}
        self.fields['titulo_tesis'].required = True
        # self.fields['archivo'].widget.label = u"Subir Tesis"
        # self.fields['archivo'].widget.attrs = {'class': 'form-control'}

        self.fields['especialidad_doctorado'].widget.label = u"Especialidad de Doctorado"
        self.fields['especialidad_doctorado'].widget.attrs = {'class': 'form-control'}


# ------------------------------------------------------------------------------
class TutorForm(ModelForm):
    class Meta:
        model = Tutor
        fields = ['nombre_tutor', 'telefono_tutor', 'email_tutor', 'apellidos_tutor']

    def __init__(self, *args, **kwargs):
        super(TutorForm, self).__init__(*args, **kwargs)
        self.fields['nombre_tutor'].widget.label = u"Nombre del Tutor"
        self.fields['nombre_tutor'].widget.attrs = {'class': 'form-control', 'placeholder': 'Nombre del Tutor'}
        self.fields['nombre_tutor'].required = True
        self.fields['apellidos_tutor'].widget.label = u"Apellidos"
        self.fields['apellidos_tutor'].widget.attrs = {'class': 'form-control', 'placeholder': 'Apellidos del Tutor'}
        self.fields['nombre_tutor'].required = True
        self.fields['telefono_tutor'].widget.label = u"Teléfono del Tutor"
        self.fields['telefono_tutor'].widget.attrs = {'class': 'form-control'}
        self.fields['email_tutor'].widget.label = u"Email del Tutor"
        self.fields['email_tutor'].widget.attrs = {'class': 'form-control'}
# ------------------------------------------------------------------------------
