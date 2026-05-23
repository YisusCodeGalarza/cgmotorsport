from django.contrib import admin
from .models import Evento, GaleriaFoto, Patrocinador

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'ubicacion', 'activo')
    list_filter = ('activo', 'fecha')
    search_fields = ('titulo', 'ubicacion')

@admin.register(GaleriaFoto)
class GaleriaFotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'fecha_subida')

@admin.register(Patrocinador)
class PatrocinadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'es_activo', 'sitio_web')
    list_filter = ('es_activo',)