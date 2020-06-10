# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import Group
from django.forms import *
# from django.forms.extras.widgets import SelectDateWidget
# from django.utils import timezone
# -----------------
from django.forms import ModelForm
from django.forms.utils import ErrorList
from django.views.generic import TemplateView

from apps.usuario.models import *
from .models import *
from apps.expediente.models import Tesis


class GroupsSelect(Form):
    groups = ModelChoiceField(queryset=Group.objects.all(), widget=SelectMultiple(attrs={
        'class': 'form-control select2',
        'multiple': 'multiple',
        'style': 'width: 100%'
    }))

    continente = ModelChoiceField(queryset=Continente.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))
    pais = ModelChoiceField(queryset=Pais.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = ModelChoiceField(queryset=Continente.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


# ------------------------------------------------------------------------------
# class TesisviewForm(ModelForm):
#     class Meta:
#         model = Tesis
#         fields = ['titulo_tesis', 'archivo']
#         exclude = ['especialidad_doctorado']
#
#     def __init__(self, *args, **kwargs):
#         super(TesisviewForm, self).__init__(*args, **kwargs)
#         # self.fields['especialidad_doctorado'].widget.label = u"Especialidad de Doctorado"
#         # self.fields['especialidad_doctorado'].widget.attrs = {'class': 'form-control'}
#         self.fields['titulo_tesis'].required = True
#         self.fields['titulo_tesis'].widget.label = u"Título de la Tesis"
#         self.fields['titulo_tesis'].widget.attrs = {'class': 'form-control'}
#         self.fields['archivo'].widget.label = u"Subir Archivo de la tesis"


# ------------------------------------------------------------------------------
class TesisForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        self.fields['titulo_tesis'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tesis
        fields = ['titulo_tesis', 'archivo']
        exclude = ['especialidad_doctorado']
        labels = {
            'titulo_tesis': 'Título de la tesis',
            'archivo': 'Documento',
        }
        widgets = {
            'titulo_tesis': TextInput(
                attrs={
                    'placeholder': 'Ingrese el título de la tesis',
                }
            ),
            'archivo': FileInput(
                attrs={
                    # 'placeholder': 'Ingrese el Documento',
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
