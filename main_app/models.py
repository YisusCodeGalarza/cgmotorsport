# models.py: La "Base de Datos".
# Cada clase que hereda de models.Model se convierte en una tabla en tu base de datos.
# Se conecta con: admin.py (para gestionarlos) y views.py (para leerlos y enviarlos al HTML).

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# 1. MODELO PARA EL CALENDARIO DE EVENTOS
class Evento(models.Model):
    # CharField es para texto corto, DateField para fechas, BooleanField para Verdadero/Falso.
    titulo = models.CharField(max_length=100, verbose_name="Nombre de la Carrera")
    fecha = models.DateField(verbose_name="Fecha del Evento")
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación (Ciudad/Estado)")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción de la Carrera")
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True, verbose_name="Imagen Promocional")
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

    def save(self, *args, **kwargs):
        if self.portada:
            try:
                img = Image.open(self.portada)
                if img.format != 'JPEG' or img.width > 1280 or img.height > 720:
                    img.thumbnail((1280, 720), Image.Resampling.LANCZOS)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                        
                    output = BytesIO()
                    img.save(output, format='JPEG', quality=75, optimize=True)
                    output.seek(0)
                    
                    nombre_base = self.portada.name.rsplit('.', 1)[0]
                    nuevo_nombre = f"{nombre_base}.jpg"
                    
                    self.portada = InMemoryUploadedFile(
                        output, 'ImageField', nuevo_nombre, 'image/jpeg', sys.getsizeof(output), None
                    )
            except Exception:
                pass
                
        super().save(*args, **kwargs)

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
        
    def save(self, *args, **kwargs):
        if self.imagen:
            try:
                img = Image.open(self.imagen)
                if img.format != 'JPEG' or img.width > 1920 or img.height > 1080:
                    img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                        
                    output = BytesIO()
                    img.save(output, format='JPEG', quality=75, optimize=True)
                    output.seek(0)
                    
                    nombre_base = self.imagen.name.rsplit('.', 1)[0]
                    nuevo_nombre = f"{nombre_base}.jpg"
                    
                    self.imagen = InMemoryUploadedFile(
                        output, 'ImageField', nuevo_nombre, 'image/jpeg', sys.getsizeof(output), None
                    )
            except Exception:
                pass
                
        super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if self.avatar:
            try:
                img = Image.open(self.avatar)
                if img.format != 'JPEG' or img.width > 500 or img.height > 500:
                    img.thumbnail((500, 500), Image.Resampling.LANCZOS)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                        
                    output = BytesIO()
                    img.save(output, format='JPEG', quality=75, optimize=True)
                    output.seek(0)
                    
                    nombre_base = self.avatar.name.rsplit('.', 1)[0]
                    nuevo_nombre = f"{nombre_base}.jpg"
                    
                    self.avatar = InMemoryUploadedFile(
                        output, 'ImageField', nuevo_nombre, 'image/jpeg', sys.getsizeof(output), None
                    )
            except Exception:
                pass
                
        super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if self.logo:
            try:
                img = Image.open(self.logo)
                # Respetamos el formato PNG para mantener las transparencias en los logos
                if img.width > 500 or img.height > 500:
                    img.thumbnail((500, 500), Image.Resampling.LANCZOS)
                    
                    output = BytesIO()
                    if img.format == 'PNG' or img.mode in ("RGBA", "P"):
                        img.save(output, format='PNG', optimize=True)
                        output.seek(0)
                        self.logo = InMemoryUploadedFile(output, 'ImageField', f"{self.logo.name.rsplit('.', 1)[0]}.png", 'image/png', sys.getsizeof(output), None)
                    else:
                        img.save(output, format='JPEG', quality=80, optimize=True)
                        output.seek(0)
                        self.logo = InMemoryUploadedFile(output, 'ImageField', f"{self.logo.name.rsplit('.', 1)[0]}.jpg", 'image/jpeg', sys.getsizeof(output), None)
            except Exception:
                pass
                
        super().save(*args, **kwargs)

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


# ----------------------------------------------------------------------
# NUEVO: MODELOS PARA FORMULARIOS DE CONTACTO Y PATROCINIOS
# ----------------------------------------------------------------------

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    area_interes = models.CharField(max_length=50, verbose_name="Área de Interés")
    asunto = models.CharField(max_length=150, verbose_name="Asunto")
    mensaje = models.TextField(verbose_name="Mensaje")
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Envío")
    leido = models.BooleanField(default=False, verbose_name="¿Leído?")

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"{self.asunto} - {self.nombre}"

class PropuestaPatrocinio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Contacto")
    puesto = models.CharField(max_length=100, verbose_name="Puesto")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    organizacion = models.CharField(max_length=100, verbose_name="Organización / Empresa")
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Página Web")
    mensaje = models.TextField(verbose_name="Motivo de Interés")
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Envío")
    revisado = models.BooleanField(default=False, verbose_name="¿Revisado?")

    class Meta:
        verbose_name = "Propuesta de Patrocinio"
        verbose_name_plural = "Propuestas de Patrocinadores"
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"Propuesta de {self.organizacion} ({self.nombre})"

class SuscripcionNewsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    fecha_suscripcion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Suscripción")

    class Meta:
        verbose_name = "Suscriptor"
        verbose_name_plural = "Suscriptores del Newsletter"
        ordering = ['-fecha_suscripcion']

    def __str__(self):
        return self.email