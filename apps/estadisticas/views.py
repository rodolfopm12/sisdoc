#-*- coding: utf-8 -*-

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.expediente.models import Expediente


@login_required
def DetallesMatriculados(request):
     labels = ['Activo', 'Inactivo']
     data = [Expediente.objects.filter(estado=True).count(), Expediente.objects.filter(estado=False).count()]

     return render(request, 'main/estadistica_matriculado.html', {
            'labels': labels,
            'data': data,
     })
