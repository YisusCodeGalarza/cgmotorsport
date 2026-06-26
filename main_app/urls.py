# urls.py: El "Enrutador" del proyecto.
# Su trabajo es escuchar la URL que el usuario escribe en el navegador 
# y conectarla con una función específica en views.py.

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views # Importamos el archivo views.py de esta misma carpeta

urlpatterns = [
    # path('', ...) significa la ruta raíz (http://127.0.0.1:8000/).
    # Se conecta con: La función 'home' definida en views.py.
    # name='home' es un alias para poder referenciar esta URL fácilmente desde los HTML (ej: {% url 'home' %}).
    path('', views.home, name='home'),
    
    # Ruta nativa de Django para cambiar de idioma (Ejecuta un POST)
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Nueva ruta para la página de patrocinadores
    path('patrocinadores/', views.patrocinadores_view, name='patrocinadores'),
    
    # Nueva ruta para el Calendario de Carreras
    path('calendario/', views.calendario_view, name='calendario'),
    
    # Nueva ruta para la página de El Equipo
    path('equipo/', views.equipo_view, name='equipo'),
    
    # Nueva ruta para el Equipo Todoterreno
    path('todoterreno/', views.todoterreno_view, name='todoterreno'),
    
    # Nueva ruta para la página de Contacto / Redes
    path('contacto/', views.contacto_view, name='contacto'),
    
    # Rutas para el Acceso de Usuarios (Autenticación)
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    
    # Ruta para suscripción al Newsletter
    path('suscribir/', views.suscribir_newsletter, name='suscribir_newsletter'),
    
    # Rutas de la Galería Multimedia
    path('galeria/', views.galeria_view, name='galeria'),
    path('galeria/foto/<int:id>/like/', views.like_foto, name='like_foto'),
    path('galeria/foto/<int:id>/comentar/', views.comentar_foto, name='comentar_foto'),
    
    # Rutas para acciones en comentarios de Galería y Vista Detalle
    path('galeria/foto/<int:id>/detalle/', views.foto_detalle_view, name='foto_detalle'),
    path('galeria/comentario/<int:id>/editar/', views.editar_comentario, name='editar_comentario'),
    path('galeria/comentario/<int:id>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),
    path('galeria/comentario/<int:id>/reportar/', views.reportar_comentario, name='reportar_comentario'),

    # Rutas del Panel de Control Privado
    path('panel/', views.panel_home, name='panel_home'),
    path('panel/eventos/', views.panel_eventos, name='panel_eventos'),
    path('panel/eventos/editar/<int:id>/', views.panel_evento_editar, name='panel_evento_editar'),
    path('panel/eventos/eliminar/<int:id>/', views.panel_evento_eliminar, name='panel_evento_eliminar'),
    path('panel/patrocinadores/', views.panel_patrocinadores, name='panel_patrocinadores'),
    path('panel/patrocinadores/editar/<int:id>/', views.panel_patrocinador_editar, name='panel_patrocinador_editar'),
    path('panel/patrocinadores/eliminar/<int:id>/', views.panel_patrocinador_eliminar, name='panel_patrocinador_eliminar'),
    path('panel/galeria/', views.panel_galeria, name='panel_galeria'),
    path('panel/galeria/editar/<int:id>/', views.panel_album_editar, name='panel_album_editar'),
    path('panel/galeria/<int:id>/fotos/', views.panel_album_fotos, name='panel_album_fotos'),
    path('panel/galeria/foto/eliminar/<int:id>/', views.panel_foto_eliminar, name='panel_foto_eliminar'),
    path('panel/galeria/eliminar/<int:id>/', views.panel_album_eliminar, name='panel_album_eliminar'),
    path('panel/mensajes/', views.panel_mensajes, name='panel_mensajes'),
    path('panel/mensajes/leer/<int:id>/', views.panel_mensaje_leer, name='panel_mensaje_leer'),
    path('panel/mensajes/eliminar/<int:id>/', views.panel_mensaje_eliminar, name='panel_mensaje_eliminar'),
    path('panel/propuestas/', views.panel_propuestas, name='panel_propuestas'),
    path('panel/propuestas/revisar/<int:id>/', views.panel_propuesta_revisar, name='panel_propuesta_revisar'),
    path('panel/propuestas/eliminar/<int:id>/', views.panel_propuesta_eliminar, name='panel_propuesta_eliminar'),
    path('panel/suscriptores/', views.panel_suscriptores, name='panel_suscriptores'),
    path('panel/suscriptores/eliminar/<int:id>/', views.panel_suscriptor_eliminar, name='panel_suscriptor_eliminar'),

    # Interacciones universales
    path('patrocinadores/<int:id>/like/', views.like_patrocinador, name='like_patrocinador'),
    path('patrocinadores/<int:id>/comentar/', views.comentar_patrocinador, name='comentar_patrocinador'),
    path('patrocinadores/comentario/<int:id>/eliminar/', views.eliminar_comentario_patrocinador, name='eliminar_comentario_patrocinador'),
    path('seccion/<str:nombre>/like/', views.like_seccion, name='like_seccion'),
    path('seccion/<str:nombre>/comentar/', views.comentar_seccion, name='comentar_seccion'),
    path('seccion/comentario/<int:id>/eliminar/', views.eliminar_comentario_seccion, name='eliminar_comentario_seccion'),
]

# Configuramos Django para que pueda servir los archivos multimedia (imágenes subidas) durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)