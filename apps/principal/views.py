# Create your views here.
# def home(request):
#     data = {}
#     return render(request, 'index.html', data)
from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

#Error
def error_404(request, exception):
    return render(request, '404.html')