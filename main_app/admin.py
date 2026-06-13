import random
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect

from .models import (
    Evento,
    Album,
    Fotografia,
    Patrocinador,
    Perfil,
    SeccionInteractiva,
    ComentarioSeccion,
    ComentarioPatrocinador,
    ComentarioFoto
)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'ubicacion', 'activo')
    list_filter = ('activo', 'fecha')
    search_fields = ('titulo', 'ubicacion')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'evento', 'fecha_creacion')
    list_filter = ('fecha_creacion', 'evento')
    search_fields = ('titulo', 'descripcion')
    
    # Usaremos un template personalizado para agregar un botón de "Subida Masiva"
    change_form_template = "admin/album_change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:album_id>/subida-masiva/', self.admin_site.admin_view(self.subida_masiva_view), name='subida_masiva_album')
        ]
        return custom_urls + urls

    def subida_masiva_view(self, request, album_id):
        album = Album.objects.get(id=album_id)
        if request.method == 'POST':
            archivos = request.FILES.getlist('fotos')
            for archivo in archivos:
                # Determinamos si es un video por la extensión del archivo
                es_video = str(archivo.name).lower().endswith(('.mp4', '.mov', '.avi', '.webm'))
                if es_video:
                    Fotografia.objects.create(album=album, archivo_video=archivo, es_video=True)
                else:
                    Fotografia.objects.create(album=album, imagen=archivo)
                    
            self.message_user(request, f"¡Se subieron {len(archivos)} archivos exitosamente al álbum '{album.titulo}'!")
            return redirect('..')
            
        context = dict(self.admin_site.each_context(request), album=album)
        return render(request, 'admin/subida_masiva_album.html', context)

@admin.register(Fotografia)
class FotografiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'album', 'fecha_subida', 'leyenda')
    list_filter = ('album', 'fecha_subida')

@admin.register(ComentarioFoto)
class ComentarioFotoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'foto', 'fecha_creacion')
    list_filter = ('fecha_creacion',)

@admin.register(Patrocinador)
class PatrocinadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'es_activo', 'sitio_web')
    list_filter = ('es_activo',)
    search_fields = ('nombre', 'descripcion', 'red_social_usuario')


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'avatar')
    search_fields = ('usuario__username', 'usuario__email')


@admin.register(SeccionInteractiva)
class SeccionInteractivaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(ComentarioSeccion)
class ComentarioSeccionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'seccion', 'fecha_creacion', 'reportado')
    list_filter = ('reportado', 'fecha_creacion', 'seccion')
    search_fields = ('texto', 'usuario__username')


@admin.register(ComentarioPatrocinador)
class ComentarioPatrocinadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'patrocinador', 'fecha_creacion', 'reportado')
    list_filter = ('reportado', 'fecha_creacion', 'patrocinador')
    search_fields = ('texto', 'usuario__username')