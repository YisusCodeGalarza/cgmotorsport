# models.py: La "Base de Datos".
# Cada clase que hereda de models.Model se convierte en una tabla en tu base de datos.
# Se conecta con: admin.py (para gestionarlos) y views.py (para leerlos y enviarlos al HTML).

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. MODELO PARA EL CALENDARIO DE EVENTOS
class Evento(models.Model):
    # CharField es para texto corto, DateField para fechas, BooleanField para Verdadero/Falso.
    titulo = models.CharField(max_length=100, verbose_name="Nombre de la Carrera")
    fecha = models.DateField(verbose_name="Fecha del Evento")
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación (Ciudad/Estado)")
    activo = models.BooleanField(default=True, verbose_name="Mostrar en la web")

    # Clase Meta define configuraciones adicionales de la tabla (como nombres en plural).
    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Calendario de Carreras"
        ordering = ['fecha']

    # __str__ define cómo se verá este objeto cuando lo imprimas o lo veas en el panel de administrador.
    def __str__(self):
        return f"{self.titulo} - {self.fecha.strftime('%d %b %Y')}"


# 2. NUEVOS MODELOS PARA LA GALERÍA (ESTRUCTURA DE ÁLBUMES)
class Album(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título del Álbum", help_text="Ej: Baja 1000 - 2026")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del Álbum")
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL, null=True, blank=True, related_name='albumes', verbose_name="Evento Asociado (Opcional)")
    portada = models.ImageField(upload_to='galeria/portadas/', blank=True, null=True, verbose_name="Foto de Portada")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Álbum"
        verbose_name_plural = "Álbumes de Galería"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo

class Fotografia(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='fotos', verbose_name="Álbum")
    imagen = models.ImageField(upload_to='galeria/fotos/', blank=True, null=True, verbose_name="Fotografía / Miniatura")
    es_video = models.BooleanField(default=False, verbose_name="¿Es un video?")
    archivo_video = models.FileField(upload_to='galeria/videos/', blank=True, null=True, verbose_name="Archivo de Video (MP4)")
    leyenda = models.CharField(max_length=200, blank=True, null=True, verbose_name="Pie de foto / Leyenda")
    fecha_subida = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='fotos_gustadas_v2', blank=True)

    class Meta:
        verbose_name = "Fotografía"
        verbose_name_plural = "Fotografías"
        ordering = ['-fecha_subida']

    def __str__(self):
        return self.leyenda if self.leyenda else f"Foto {self.id} del Álbum: {self.album.titulo}"

class ComentarioFoto(models.Model):
    foto = models.ForeignKey(Fotografia, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    reportado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Comentario de Galería"
        verbose_name_plural = "Comentarios de Galería"
        ordering = ['-fecha_creacion']

# NUEVO: MODELO DE PERFIL DE USUARIO
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    avatar = models.ImageField(upload_to='avatares/', blank=True, null=True, verbose_name="Foto de Perfil")

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

# SEÑAL: Crea un Perfil automáticamente cuando un Usuario se registra
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

# 3. MODELO PARA LOS PATROCINADORES
class Patrocinador(models.Model):
    # ImageField y URLField son campos especiales de Django que validan que el dato sea una imagen o URL válida.
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Patrocinador")
    logo = models.ImageField(upload_to='patrocinadores/', verbose_name="Logo Oficial")
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Enlace Web (Opcional)")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción", help_text="Ej: Apoyando al equipo en cada carrera...")
    red_social_usuario = models.CharField(max_length=50, blank=True, null=True, verbose_name="Usuario de Red Social", help_text="Ej: @mirage")
    red_social_url = models.URLField(blank=True, null=True, verbose_name="Enlace de la Red Social")
    es_activo = models.BooleanField(default=True, verbose_name="Patrocinador Activo")
    likes = models.ManyToManyField(User, related_name='patrocinadores_gustados', blank=True)

    class Meta:
        verbose_name = "Patrocinador"
        verbose_name_plural = "Patrocinadores"

    def __str__(self):
        return self.nombre

class ComentarioPatrocinador(models.Model):
    patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    reportado = models.BooleanField(default=False)

    class Meta:
        ordering = ['fecha_creacion']

class SeccionInteractiva(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Identificador de la Sección")
    likes = models.ManyToManyField(User, related_name='secciones_gustadas', blank=True)
    
    class Meta:
        verbose_name = "Sección Interactiva"
        verbose_name_plural = "Secciones Interactivas"
        
    def __str__(self):
        return self.nombre.capitalize()

class ComentarioSeccion(models.Model):
    seccion = models.ForeignKey(SeccionInteractiva, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    reportado = models.BooleanField(default=False)