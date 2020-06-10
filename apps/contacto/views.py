from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
#View de Contacto
def contacto(request):
    if request.method == "POST":
        subject = request.POST["nombre"]
        message = request.POST["mensaje"] + " " + request.POST["email"]
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ["ileca@ensap.sld.cu"]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, "gracias.html")
    return render(request, "contacto.html")
