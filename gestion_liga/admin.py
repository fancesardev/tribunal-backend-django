from django.contrib import admin
# Importa los modelos que acabas de definir en models.py
from .models import Equipo, Jugador, Resolucion, Sancion

# Registra cada modelo para que aparezca en el panel de administración
admin.site.register(Equipo)
admin.site.register(Jugador)
admin.site.register(Resolucion)
admin.site.register(Sancion)