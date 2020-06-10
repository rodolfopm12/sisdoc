"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.staticfiles import views as static_views
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve
from django.conf import settings

# Del sitio
# from apps.login.views import LoginFormView
from apps.principal import views as principal_views
from apps.principal.views import IndexView
from apps.usuario import views
from django.conf.urls.static import static

urlpatterns = [
    # path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # il8n
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),  # Interna
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('login/', include('apps.login.urls')),
    path('contacto/', include('apps.contacto.url'), name='contacto'),
    path('inicio/', include('apps.usuario.url'), name='inicio'),
    path('expediente/', include('apps.expediente.urls'), name='expediente'),
    path('tesis/', include('apps.tesis.url'), name='tesis'),
    path('estadistica/', include('apps.estadisticas.urls'), name='estadisticas'),
    path('reporte/', include('apps.reportes.urls'), name='reporte'),
]
handler404 = 'apps.principal.views.error_404'
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += [
#         url(r'^static/(?P<path>.*)$', static_views.serve),
#         url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#
#     ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns