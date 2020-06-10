# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, TemplateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.expediente.models import Tesis, Pais, Continente
from apps.tesis.forms import GroupsSelect, TesisForm


class TestView(TemplateView):
    template_name = 'tests.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GroupsSelect()
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product_id':
                data = [{'id': '', 'text': '------------'}]
                for i in Pais.objects.filter(cat_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.name, 'data': i.pais.toJSON()})
            elif action == 'autocomplete':
                data = []
                for i in Continente.objects.filter(name__icontains=request.POST['term'])[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Select Aninados | Django'
        context['form'] = GroupsSelect()
        return context


class CrearTesis(LoginRequiredMixin, CreateView):
    model = Tesis
    form_class = TesisForm
    template_name = 'subir_tesis.html'
    success_url = reverse_lazy('tesis:listar_tesis')

    # queryset = Tesis.objects.filter(request.user)

    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'crear':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Subir Tesis'
        context['crear_url'] = reverse_lazy('tesisview')
        context['etiqueta'] = 'Agregar Tesis'
        context['entidad'] = 'Tesis'
        context['list_url'] = reverse_lazy('listar_tesis')
        context['action'] = 'crear'
        return context


# ----------------------------------------------------------------------------------------------------
# -----------------------Listar Expediente------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
class ListarTesis(LoginRequiredMixin, ListView):
    model = Tesis
    template_name = 'listar_tesis.html'
    context_object_name = 'tesis'
    queryset = Tesis.objects.filter()

    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listados de Tesis'
        context['crear_url'] = reverse_lazy('tesisview')
        context['entidad'] = 'Tesis'
        context['etiqueta'] = 'Crear Tesis'
        context['list_url'] = reverse_lazy('listar_tesis')
        return context


# ----------------------------------------------------------------------------------------------------
# ----------------------- Eliminar Tesis---------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
class EliminarTesis(LoginRequiredMixin, DeleteView):
    model = Tesis
    template_name = 'eliminar_tesis.html'
    success_url = reverse_lazy('listar_tesis')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Tesis'
        context['entidad'] = 'Tesis'
        context['list_url'] = reverse_lazy('listar_tesis')
        context['action'] = 'eliminar'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
