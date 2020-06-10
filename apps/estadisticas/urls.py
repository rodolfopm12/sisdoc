
from django.urls import path
# from apps.estadisticas import views
from apps.estadisticas import views
from apps.estadisticas.views import DetallesMatriculados

urlpatterns = [
    path('grafico/', views.DetallesMatriculados, name='destalles_matriculados'),

]
