from django.conf.urls import url
# from  django.urls import path, re_path
from django.urls import path

# from apps.main import views
from apps.usuario import views
from apps.usuario.views import Inicio, ListaUsuarios, RegistroUsuario, Perfil, EditarUsuarios, EliminarUsuario

urlpatterns = [
    # url('inicio', views.inicio, name='inicio'),
    path('', Inicio.as_view(), name='inicio'),
    path('perfil/', Perfil.as_view(), name='perfil'),
    url(r'^perfil/edit/$', views.editar_perfil, name='editar_user'),
    # # path('register/', register, name='register'),
    path('register/', RegistroUsuario.as_view(), name='register'),
    path('eliminar_usuario/<int:pk>/', EliminarUsuario.as_view(), name='eliminar_usuario'),
    path('listado_usuarios/', ListaUsuarios.as_view(), name='listado_usuarios'),
    path('edit_usuario/<int:pk>/', EditarUsuarios.as_view(), name='usuarios_update'),
    # path('editar_expediente/<int:pk>/', EditarExpediente.as_view(), name='editar_expediente'),
    # path('eliminar_expediente/<int:pk>/', EliminarExpediente.as_view(), name='eliminar_expediente'),

]
