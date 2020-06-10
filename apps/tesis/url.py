# from django.conf.urls import url
# from  django.urls import path, re_path
from django.urls import path

# from apps.main import views
# from apps.usuario.views import Inicio, Perfil, RegistroUsuario, ListaUsuarios
from apps.tesis.views import CrearTesis, ListarTesis, TestView, EliminarTesis

urlpatterns = [
    path('actualizar_tesis/', CrearTesis.as_view(), name='tesisview'),
    path('listar_tesis/', ListarTesis.as_view(), name='listar_tesis'),
    # path('editar_expediente/<int:pk>/', EditarTesis.as_view(), name='editar_expediente'),
    path('eliminar_tesis/<int:pk>/', EliminarTesis.as_view(), name='eliminar_tesis'),
    path('test/', TestView.as_view(), name='testselect'),
]
