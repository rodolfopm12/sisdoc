import os
from datetime import date

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse_lazy
from xhtml2pdf import pisa

# ------------------------
from django.views.generic.base import View, TemplateView

from apps.expediente.models import Expediente
from apps.usuario.models import User

class Index(LoginRequiredMixin, TemplateView):
    template_name = 'reportes.html'


class InvoicePDFView(LoginRequiredMixin, View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('pdf/pdf_template.html')
            context = {
                # 'expediente': Expediente.objects.get(pk=self.kwargs['pk']),
                'expediente': Expediente.objects.count(),
                'expediente_act' : Expediente.objects.filter(estado=True).count(),
                'expediente_des' : Expediente.objects.filter(estado=False).count(),
                'cantidad_usuarios' : User.objects.count(),
                'cantidad_usuarios_act' : User.objects.filter(is_active=True).count(),
                'cantidad_usuarios_des' : User.objects.filter(is_active=False).count(),
                'title': 'Datos Generales del sistema',
                'comp': {'name': 'Escuela Nacional de Salud Pública', 'sistema': 'Sistema de Doctorado (SISDOC)',
                         'address': 'Calle 100 # 1032 e/ Perla y E, Altahabana, Boyeros, La Habana, Cuba'},
                'email': request.user.email,
                'website': "sisdoc.ensap.sld.cu",
                'fecha': date.today,
                'user': request.user.first_name + request.user.last_name,
                'icon': '{}{}'.format(settings.STATIC_URL, 'img/logo-ensap.png'),
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
            # create a pdf
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            # if error then show some funy view
            # if pisaStatus.err:
            #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('inicio'))
