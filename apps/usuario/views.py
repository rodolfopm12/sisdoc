# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages

from apps import usuario
from django.contrib.auth.models import *
from apps.expediente.models import Expediente
from apps.usuario.forms import CrearUsuarioForm, ProfileForm, EditProfileForm
from apps.usuario.models import User, UserProfile


# from apps.usuario.forms import CrearUsuarioForm, ProfileForm

# Create your views here.
class Inicio(TemplateView):
    template_name = 'main/inicio.html'
    model = Expediente

    # cantidad_expedientes = Expediente.objects.filter(estado=True).count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cantidad_expedientes'] = Expediente.objects.filter(estado=True).count()
        context['cantidad_usuarios'] = User.objects.count()
        return context


# ---------------------------------------------------------------------------------------------
class ListaUsuarios(LoginRequiredMixin, ListView):
    model = User
    template_name = 'usuarios_registrados.html'
    context_object_name = 'users'

    # paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(is_active=True).exclude(is_superuser=True)

    # queryset = User.objects.filter(is_active=True).exclude(is_superuser=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['crear_url'] = reverse_lazy('register')
        context['list_url'] = reverse_lazy('listado_usuarios')
        context['etiqueta'] = 'Crear Usuario'
        context['action'] = 'crear'
        return context


# ----------------------------------------------------------------------------------------------------
# ----------------------- Editar Usuario -------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
def editar_perfil(request):
    if request.method == 'POST':
        # formulario enviado
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # Formulario validado correctamente
            form.save()
            return redirect('perfil')
    else:
        # formulario inicial
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'edit_profile.html', args)
# ----------------------------------------------------------------------------------------------------
# ----------------------- Editar Usuarios dentro del listado -----------------------------------------
# ----------------------------------------------------------------------------------------------------
class EditarUsuarios(UpdateView):
    model = User
    form_class = CrearUsuarioForm
    template_name = 'editar_usuario.html'
    success_url = reverse_lazy('listado_usuarios')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Usuario'
        context['entidad'] = 'Usuarios'
        context['list_url'] = reverse_lazy('listado_usuarios')
        context['action'] = 'edit'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

# ---------------------------------------------------------------------------------------------
class RegistroUsuario(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = CrearUsuarioForm
    # profile_form = ProfileForm
    sucecess_url = reverse_lazy('listado_usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de usuario'
        context['create_url'] = reverse_lazy('register')
        context['etiqueta'] = 'Crear Usuario'
        context['entidad'] = 'Registro de usuario'
        context['list_url'] = reverse_lazy('listado_usuarios')
        context['action'] = 'crear'
        # context['grupos'] = Group.objects.all()
        # context['form'] = CrearUsuarioForm()
        context['form2'] = ProfileForm()
        return context

    def get_success_url(self):
        return reverse_lazy('listado_usuarios')
# ---------------------------------------------------------------------------------------------
class EliminarUsuario(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'eliminar_usuario.html'
    success_url = reverse_lazy('listado_usuarios')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Usuario'
        context['entidad'] = 'Usuario'
        context['list_url'] = reverse_lazy('listado_usuarios')
        context['action'] = 'eliminar'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
# ---------------------------------------------------------------------------------------------

# @login_required
# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             return redirect('inicio')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {
#         'form': form
#     })
# ---------------------------------------------------------------------------------------------
class Perfil(LoginRequiredMixin, TemplateView):
    model = UserProfile
    template_name = 'perfil.html'
