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
    
    # Rutas de la Galería Multimedia
    path('galeria/', views.galeria_view, name='galeria'),
    path('galeria/foto/<int:id>/like/', views.like_foto, name='like_foto'),
    path('galeria/foto/<int:id>/comentar/', views.comentar_foto, name='comentar_foto'),
    
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