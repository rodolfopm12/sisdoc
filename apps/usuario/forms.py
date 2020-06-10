# -*- coding: utf-8 -*-
from django import forms
# from django.forms import *
from django.forms.utils import ErrorList

from django.forms import ModelForm, SelectMultiple
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from apps.expediente.models import Doctorando
from .models import *
from .models import User


# ----------------------------------------------------------------------------------
class CrearUsuarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['email'].widget.attrs['autofocus'] = True

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    groups = forms.ModelChoiceField(queryset=Group.objects.all(), widget=SelectMultiple(attrs={
        'class': 'select2',
        'multiple': 'multiple',
        'style': 'width: 100%'
    }))

    class Meta:
        model = User
        fields = ('image', 'email', 'first_name', 'last_name', 'password1', 'password2', 'groups', 'is_active')
        labels = {'image': 'Foto de Perfil',
                  'email': 'Correo',
                  'first_name': 'Nombre',
                  'last_name': 'Apellidos',
                  'groups': 'Rol',
                  }

    def save(self, commit=True):
        user = super(CrearUsuarioForm, self).save(commit=False)
        user.image = self.cleaned_data['image']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.groups = self.cleaned_data['groups']
        user.is_active = self.cleaned_data['is_active']

        if commit:
            user.save()
        return user


# ----------------------------------------------------------------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('sexo', 'nota')

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

# ----------------------------------------------------------------------------------
class EditProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['email'].widget.attrs['autofocus'] = True

    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('image', 'email', 'first_name', 'last_name', 'password')

# class UserForm(ModelForm):
#     """User form."""
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name',]
#
#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].required = True
#         self.fields['last_name'].required = True
# self.fields['email'].required = True

# ----------------------------------------------------------------------------------
# class UserEditForm(ModelForm):
#     """User form."""
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name',]
#
#     def __init__(self, *args, **kwargs):
#         super(UserEditForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].required = True
#         self.fields['last_name'].required = True
# self.fields['email'].required = True
# ----------------------------------------------------------------------------------
# class UserProfileForm(ModelForm):
#     """User profile form."""
#     class Meta:
#         model = Profile
#         exclude = ('User')
#
#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         self.fields['nota'].widget.label = u"Nota"
#         self.fields['nota'].widget.attrs = {'rows': '3'}
# self.fields['sexo'].widget.attrs = {'class': 'chosen-select', }
# self.fields['profesion'].widget.attrs = {'class': 'chosen-select', }
# self.fields['especialidad'].widget.attrs = {'class': 'chosen-select', }
# self.fields['cargo'].widget.attrs = {'class': 'chosen-select', }
# self.fields['grado_cientifico'].widget.attrs = {'class': 'chosen-select', }
# self.fields['fecha_nacimiento'].widget.attrs = {'class': 'date-picker', }
