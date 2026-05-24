# admin.py: El "Panel de Control".
# Aquí registramos nuestros modelos para que Django cree automáticamente un panel de gestión visual.
# Se conecta con: models.py (importa las clases creadas allí).

from django.contrib import admin
from .models import Evento, GaleriaFoto, Patrocinador

# Usamos decoradores (@admin.register) para registrar el modelo.
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    # list_display: Columnas que se mostrarán en la lista principal del administrador.
    list_display = ('titulo', 'fecha', 'ubicacion', 'activo')
    # list_filter: Agrega una barra lateral para filtrar resultados rápidamente.
    list_filter = ('activo', 'fecha')
    # search_fields: Agrega una barra de búsqueda en la parte superior.
    search_fields = ('titulo', 'ubicacion')

@admin.register(GaleriaFoto)
class GaleriaFotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'evento', 'fecha_subida')
    list_filter = ('evento', 'fecha_subida')

@admin.register(Patrocinador)
class PatrocinadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'es_activo', 'sitio_web')
    list_filter = ('es_activo',)