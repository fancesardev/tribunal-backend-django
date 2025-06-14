from rest_framework import serializers
from .models import Equipo, Jugador, Resolucion, Sancion

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

class JugadorSerializer(serializers.ModelSerializer):
    # 'equipo_nombre' ahora se obtiene de la @property en el modelo Jugador
    # Esto es más robusto que source='equipo.nombre'
    equipo_nombre = serializers.ReadOnlyField() 
    
    # 'equipo_categoria' es la categoría del EQUIPO, no la del jugador.
    # Si quieres la categoría del JUGADOR, el campo 'categoria' ya está en el modelo Jugador.
    # Si esta es la categoría del EQUIPO, déjala así. Si querías la categoría del JUGADOR,
    # el campo 'categoria' ya lo mapearemos directamente.
    equipo_categoria = serializers.CharField(source='equipo.categoria', read_only=True) 

    class Meta:
        model = Jugador
        fields = [
            'id_jugador', 
            'codigo_socio', # <--- ¡IMPORTANTE! Cambiado de 'numero_socio' a 'codigo_socio'
            'apellido', 
            'nombre', 
            'equipo', # Mantén el id del equipo para poder crear/editar Jugadores
            'equipo_nombre', 
            'equipo_categoria', # Si quieres la categoría del equipo
            'categoria', # <--- ¡IMPORTANTE! Añade la categoría del JUGADOR
        ]

class ResolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resolucion
        fields = '__all__'

class SancionSerializer(serializers.ModelSerializer):
    jugador_detail = JugadorSerializer(source='jugador', read_only=True)
    resolucion_detail = ResolucionSerializer(source='resolucion', read_only=True)
    estado_calculado = serializers.SerializerMethodField()
    fechas_restantes = serializers.SerializerMethodField()

    class Meta:
        model = Sancion
        fields = [
            'id_sancion',
            'jugador',
            'resolucion',
            'fecha_inicio',
            'fecha_fin',
            'descripcion',
            'estado',
            'tipo_sancion',
            'doble_amarilla_pagada',
            'fecha_pago_doble_amarilla',
            'cantidad_fechas',
            'jugador_detail',
            'resolucion_detail',
            'estado_calculado',
            'fechas_restantes',
        ]

        extra_kwargs = {
            'resolucion': {'required': False, 'allow_null': True},
            'fecha_fin': {'read_only': True},
        }

    def get_estado_calculado(self, obj):
        return obj.estado_calculado
    
    def get_fechas_restantes(self, obj):
        return obj.fechas_restantes