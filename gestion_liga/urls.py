from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestion_liga.views import EquipoViewSet, JugadorViewSet, ResolucionViewSet, SancionViewSet

# Crea un enrutador (router) y registra tus ViewSets con él.
# Esto genera automáticamente las URLs para las operaciones CRUD.
router = DefaultRouter()
router.register(r'equipos', EquipoViewSet)
router.register(r'jugadores', JugadorViewSet)
router.register(r'resoluciones', ResolucionViewSet)
router.register(r'sanciones', SancionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]