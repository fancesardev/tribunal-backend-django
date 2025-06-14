"""
URL configuration for tribunal_liga_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestion_liga.views import EquipoViewSet, JugadorViewSet, ResolucionViewSet, SancionViewSet  # Importa JugadorViewSet

from django.views.generic.base import RedirectView


router = DefaultRouter()
router.register(r'equipos', EquipoViewSet)
router.register(r'jugadores', JugadorViewSet) # <--- Añade esta línea
router.register(r'resoluciones', ResolucionViewSet)
router.register(r'sanciones', SancionViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', RedirectView.as_view(url='api/sanciones/', permanent=False), name='api_root_redirect'),
    # Si quisieras una página de inicio real, tendrías que definir una vista (ej. index)
]
