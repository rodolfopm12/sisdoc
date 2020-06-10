from django.conf.urls import url
from django.urls import path, re_path
from apps.expediente import views
from apps.expediente.views import ListarExpediente, ExpedientesActivos, ExpedientesDesactivados, EditarExpediente, \
    EliminarExpediente, CrearExpediente, CrearTest

urlpatterns = [
    # url('home', views.inicio, name='inicio'),
    # url('crear', views.crear_expediente, name='crear_expediente'),

    path('crear/', CrearExpediente.as_view(), name='crear_expediente'),
    #path('creartest/', CrearTest.as_view(), name='creartest'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('listar_expedientes/', ListarExpediente.as_view(), name='listar_expedientes'),
    path('editar_expediente/<int:pk>/', EditarExpediente.as_view(), name='editar_expediente'),
    path('eliminar_expediente/<int:pk>/', EliminarExpediente.as_view(), name='eliminar_expediente'),
    #####path('eliminar_expediente/<int:id>', views.eliminar_expediente, name='eliminar_expediente'),

    path('expediente_activo/', ExpedientesActivos.as_view(), name='expedientes_activos'),
    path('expediente_desactivados/', ExpedientesDesactivados.as_view(), name='expedientes_desactivados'),
    # path('estadistica/', views.DetallesMatriculados, name='destalles_matriculados'),
    #####url('expediente_activo/', views.expediente_activo, name='expediente_activo'),
    path('ajax/load-pais/', views.load_pais, name='ajax_load_pais'),
    path('ajax/load-estado/', views.load_estado, name='ajax_load_estados'),
    path('ajax/load-municipio/', views.load_municipio, name='ajax_load_municipio'),

    # url('listar_expedientes', views.listar_expedientes, name='listar_expedientes'),
    # path('editar_expediente/<int:id>', views.editar_expediente, name='editar_expediente'),
    # path('editar_expediente/<int:id>', views.editar_expediente, name='editar_expediente'),
    # url('editar_expediente', views.editar_expediente, name = 'editar_expediente'),
    # url('eliminar_expediente', views.eliminar_expediente, name='eliminar_expediente'),
    # url('', views.expediente, name='expediente'),
]
