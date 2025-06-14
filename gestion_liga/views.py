from rest_framework import viewsets
from .models import Equipo, Jugador, Resolucion, Sancion
from .serializers import EquipoSerializer, JugadorSerializer, ResolucionSerializer, SancionSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all() # Consulta todos los objetos de Equipo
    serializer_class = EquipoSerializer # Usa el EquipoSerializer para serializar/deserializar

class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer

class ResolucionViewSet(viewsets.ModelViewSet):
    queryset = Resolucion.objects.all()
    serializer_class = ResolucionSerializer

class SancionViewSet(viewsets.ModelViewSet):
    queryset = Sancion.objects.all()
    serializer_class = SancionSerializer