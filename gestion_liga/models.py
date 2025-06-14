from django.db import models
from datetime import timedelta, date

class Equipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50) 

    class Meta:
        db_table = 'equipos'
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'

    def __str__(self):
        return self.nombre

class Jugador(models.Model):
    CATEGORIA_CHOICES = [
        ('C33', 'Categoría C33'),
        ('C40', 'Categoría C40'),
        ('C45', 'Categoría C45'),
    ]

    id_jugador = models.AutoField(primary_key=True)
    # MODIFICACIÓN: Hazlo null=True y blank=True para la migración inicial
    codigo_socio = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Código de Socio") 
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES, default='C40')

    class Meta:
        db_table = 'jugadores'
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.equipo.nombre})"
    
    @property
    def equipo_nombre(self):
        return self.equipo.nombre if self.equipo else None

class Resolucion(models.Model):
    id_resolucion = models.AutoField(primary_key=True)
    numero_resolucion = models.CharField(max_length=100, unique=True)
    fecha_resolucion = models.DateField()
    descripcion = models.TextField()

    class Meta:
        db_table = 'resoluciones'
        verbose_name = 'Resolución'
        verbose_name_plural = 'Resoluciones'

    def __str__(self):
        return f"Resolución N° {self.numero_resolucion} del {self.fecha_resolucion}"

class Sancion(models.Model):
    TIPO_SANCION_CHOICES = [
        ('Doble Amarilla', 'Doble Amarilla'),
        ('Provisorio', 'Provisorio'),
        ('Definitiva', 'Definitiva'),
    ]

    id_sancion = models.AutoField(primary_key=True)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=50, default='Pendiente')
    tipo_sancion = models.CharField(max_length=50, choices=TIPO_SANCION_CHOICES, default='Definitiva')
    doble_amarilla_pagada = models.BooleanField(default=False)
    fecha_pago_doble_amarilla = models.DateField(null=True, blank=True)
    cantidad_fechas = models.IntegerField(default=0)

    class Meta:
        db_table = 'sanciones'
        verbose_name = 'Sanción'
        verbose_name_plural = 'Sanciones'

    def __str__(self):
        return f"Sanción a {self.jugador.apellido} {self.jugador.nombre} - {self.tipo_sancion}"

    @property
    def estado_calculado(self):
        hoy = date.today()
        if self.tipo_sancion == 'Doble Amarilla':
            return 'Pagada' if self.doble_amarilla_pagada else 'Pendiente'
        elif self.fecha_inicio and self.fecha_fin:
            if hoy < self.fecha_inicio:
                return 'Pendiente'
            elif self.fecha_inicio <= hoy <= self.fecha_fin:
                return 'Activa'
            else: # hoy > self.fecha_fin
                return 'Cumplida'
        return 'Estado Desconocido'

    @property
    def fechas_restantes(self):
        hoy = date.today()
        if self.tipo_sancion in ['Provisorio', 'Definitiva'] and self.fecha_fin:
            dias_restantes = (self.fecha_fin - hoy).days
            if dias_restantes > 0:
                return (dias_restantes + 6) // 7
            else:
                return 0
        return None

    def save(self, *args, **kwargs):
        if self.tipo_sancion in ['Provisorio', 'Definitiva'] and self.cantidad_fechas > 0 and self.fecha_inicio:
            self.fecha_fin = self.fecha_inicio + timedelta(weeks=self.cantidad_fechas)
        elif self.tipo_sancion == 'Doble Amarilla' or self.cantidad_fechas == 0:
            self.fecha_fin = None

        super().save(*args, **kwargs)