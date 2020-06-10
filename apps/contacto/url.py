from django.urls import path
from apps.contacto.views import contacto

urlpatterns = [
    path('', contacto, name='contacto'),
]

