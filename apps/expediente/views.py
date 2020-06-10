# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, View
from apps.expediente.models import *

from apps.expediente.forms import ExpedienteForm, DoctorandoForm, \
    CategoriaInvestigadorForm, EspecialidadForm, \
    TesisForm, TutorForm, CentroTrabajoForm, UserForm, ProfileForm


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse(
            'Gracias por su correo electrónico de confirmación. Ahora puede iniciar sesión en su cuenta.')
    else:
        return HttpResponse('El enlace de activación no es válido.!')


class CrearTest(CreateView):
    model = Expediente
    form_class = ExpedienteForm
    template_name = 'creartest.html'
    success_url = reverse_lazy('listar_expedientes')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['title'] = 'Hoja Anexo 2'
        context['crear_url'] = reverse_lazy('creartest')
        context['etiqueta'] = 'Crear Expediente'
        context['entidad'] = 'Expedientes'
        context['list_url'] = reverse_lazy('listar_expedientes')
        context['action'] = 'crear'
        return context


# ----------------------------------------------------------------------------------------------------
# -----------------------Crear Expediente-------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
class CrearExpediente(CreateView):
    model = Expediente
    template_name = 'crear_expediente1.html'
    form_class = ExpedienteForm
    second_form_class = UserForm
    third_form_class = ProfileForm
    four_form_class = DoctorandoForm
    five_form_class = CentroTrabajoForm
    # six_form_class = TesisForm
    seven_form_class = TutorForm
    success_url = reverse_lazy('expediente:listar_expedientes')

    def get_context_data(self, **kwargs):
        context = super(CrearExpediente, self).get_context_data(**kwargs)
        context['title'] = 'Hoja Anexo 2'
        context['crear_url'] = reverse_lazy('crear_expediente')
        context['etiqueta'] = 'Crear Expediente'
        context['entidad'] = 'Expedientes'
        context['list_url'] = reverse_lazy('listar_expedientes')
        context['action'] = 'crear'
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(self.request.GET)
        if 'form4' not in context:
            context['form4'] = self.four_form_class(self.request.GET)
        if 'form5' not in context:
            context['form5'] = self.five_form_class(self.request.GET)
        # if 'form6' not in context:
        #     context['form6'] = self.six_form_class(self.request.GET)
        if 'form7' not in context:
            context['form7'] = self.seven_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        form3 = self.third_form_class(request.POST)
        form4 = self.four_form_class(request.POST)
        form5 = self.five_form_class(request.POST)
        # form6 = self.six_form_class(request.POST)
        form7 = self.seven_form_class(request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid() and form7.is_valid():
            expediente = form.save(commit=False)
            # expediente_user = form2.save(commit=False)
            expediente_profile = form3.save(commit=False)
            expediente_datos = form4.save(commit=False)
            expediente__centro_trabajo = form5.save(commit=False)
            # expediente__tesis = form6.save(commit=False)
            expediente__tutor = form7.save(commit=False)
            expediente.save()
            user = form2.save(commit=False)
            user.is_active = False
            password = User.objects.make_random_password(15)
            user.save()
            group = Group.objects.get(pk=3)
            user.groups.add(group)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse(
                'Confirme su dirección de correo electrónico para completar el registro.') + HttpResponseRedirect(
                self.get_success_url())
            # return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2, form3=form3, form4=form4, form5=form5, form7=form7))


def load_pais(request):
    continente_id = request.GET.get('continente')
    paises = Pais.objects.filter(continente_id=continente_id).order_by('nombre')
    return render(request, 'hr/pais_dropdown_list.html', {'paises': paises})


def load_estado(request):
    pais_id = request.GET.get('pais')
    provincias = Provincia.objects.filter(pais_id=pais_id).order_by('nombre')
    return render(request, 'hr/estado_dropdown_list.html', {'provincias': provincias})


def load_municipio(request):
    provincia_id = request.GET.get('provincia')
    municipios = Municipio.objects.filter(provincia_id=provincia_id).order_by('nombre')
    return render(request, 'hr/municipio_dropdown_list.html', {'municipios': municipios})


# ----------------------------------------------------------------------------------------------------
# -----------------------Listar Expediente------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
class ListarExpediente(ListView):
    model = Expediente
    template_name = 'listar_expediente.html'

    # context_object_name = 'expedientes'
    # queryset = Expediente.objects.all()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listados de Expedientes'
        context['crear_url'] = reverse_lazy('crear_expediente')
        context['entidad'] = 'Expedientes'
        context['etiqueta'] = 'Crear Expedientes'
        context['list_url'] = reverse_lazy('listar_expedientes')
        return context

    # paginate_by = 3

    # def paginatorexpediente(request):
    #     expediente_list = Expediente.objects.all()
    #     page = request.GET.get('page', 1)
    #     paginator = Paginator(Expediente, 2)
    #     try:
    #         expediente = paginator.page(page)
    #     except PageNotAnInteger:
    #         expediente = paginator.page(1)
    #     except EmptyPage:
    #         expediente = paginator.page(paginator.num_pages)
    #     return render(request, 'expediente/listar_expediente.html', {'expdiente':expediente})


class ExpedientesActivos(ListView):
    model = Expediente
    template_name = 'expediente_activo.html'

    # context_object_name = 'expedientes'
    # queryset = Expediente.objects.filter(estado = True)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Expediente.objects.filter(estado=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Expedientes Activos'
        return context


class ExpedientesDesactivados(ListView):
    model = Expediente
    template_name = 'expediente_desactivado.html'

    # context_object_name = 'expedientes'
    # queryset = Expediente.objects.filter(estado=False)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Expediente.objects.filter(estado=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Expedientes Desactivados'
        return context


# def get(self, request, *args, **kwargs):
#     #expedientes = Expediente.objects.filter(estado = True)
#     expedientes = Expediente.objects.all()
#     return render(request, self.template_name, {'expedientes':expedientes})

# @csrf_exempt
# def listar_expedientes(request):
#     #if request.method == 'GET':
#      #   data = {
#       #      'expediente': Expediente.objects.all()
#             #'title': 'Listado de Expedientes'
#             # , {'doctorandos':doctorando}
#        # }
#     expedientes = Expediente.objects.all()
#     return render(request, 'expediente/listar_expediente.html', {'expedientes':expedientes})
# ----------------------------------------------------------------------------------------------------
# ----------------------- Editar Expediente ------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
class EditarExpediente(UpdateView):
    model = Expediente
    form_class = ExpedienteForm
    template_name = 'crear_expediente1.html'
    success_url = reverse_lazy('listar_expedientes')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Expedientes'
        context['entidad'] = 'Expedientes'
        context['list_url'] = reverse_lazy('listar_expedientes')
        context['action'] = 'edit'
        return context

    def get_form_kwargs(self):
        # Este metodo se asegura que se pase el objeto existente al crear el formulario
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs


# ----------------------------------------------------------------------------------------------------
# ----------------------- Eliminar Expediente---------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
class EliminarExpediente(LoginRequiredMixin, DeleteView):
    model = Expediente
    template_name = 'eliminar_expediente.html'
    success_url = reverse_lazy('listar_expedientes')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Expedientes'
        context['entidad'] = 'Expedientes'
        context['list_url'] = reverse_lazy('listar_expedientes')
        context['action'] = 'eliminar'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # self.object.delete()
            self.object.estado = False
            self.object.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    # def post(self, request, pk, *args, **kwargs):
    #     object = Expediente.objects.get(id=pk)
    #     object.estado = False
    #     object.save()
    #     return redirect('listar_expedientes')

# @csrf_exempt
# def eliminar_expediente(request, id):
#     expediente = Expediente.objects.get(id = id)
#     expediente.delete()
#     return redirect('expediente:listar_expedientes')
# ----------------------------------------------------------------------------------------------------
