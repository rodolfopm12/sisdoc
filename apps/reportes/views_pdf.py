import os
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.conf import settings
from django.template import Context

from datetime import datetime
import datetime


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


data = {
    "company": "Escuela Nacional de Salud Pública",
    "address": "Calle 100 # 1032 e/ Perla y E, Altahabana, Boyeros, La Habana, Cuba",
    "city": "La Habana",
    "state": "WA",
    "zipcode": "98663",
    "phone": "(53) 7643 1429-30-31",
    "email": "doctorado@ensap.sld.cu",
    "website": "sisdoc.ensap.sld.cu",
    "Fecha_actual": '%d/%m/%Y',
}


def link_callback(uri, rel):
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mRoot = settings.MEDIA_ROOT
    mUrl = settings.MEDIA_URL

    if uri.startswitch(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswitch(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception(
            'media URL must start with %s or %s' % (sUrl, mUrl)
        )
    return path


# Opens up page as PDF
class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('pdf/pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('pdf/pdf_template.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename= %s" % (filename)
        response['Content-Disposition'] = content
        return response


def index(request):
    context = {}
    return render(request, 'pdf/index.html', context)

