from django.db import models

# 1. MODELO PARA EL CALENDARIO DE EVENTOS
class Evento(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Nombre de la Carrera")
    fecha = models.DateField(verbose_name="Fecha del Evento")
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación (Ciudad/Estado)")
    activo = models.BooleanField(default=True, verbose_name="Mostrar en la web")

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Calendario de Carreras"
        ordering = ['fecha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.titulo} - {self.fecha.strftime('%d %b %Y')}"


# 2. MODELO PARA LA GALERÍA DE FOTOS (Aquí subirá sus tomas de acción)
class GaleriaFoto(models.Model):
    titulo = models.CharField(max_length=100, blank=True, verbose_name="Título de la foto")
    imagen = models.ImageField(upload_to='galeria/', verbose_name="Archivo de Imagen")
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foto de Galería"
        verbose_name_plural = "Galería de Fotos"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.titulo if self.titulo else f"Foto #{self.id}"


# 3. MODELO PARA LOS PATROCINADORES
class Patrocinador(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Patrocinador")
    logo = models.ImageField(upload_to='patrocinadores/', verbose_name="Logo Oficial")
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Enlace Web (Opcional)")
    es_activo = models.BooleanField(default=True, verbose_name="Patrocinador Activo")

    class Meta:
        verbose_name = "Patrocinador"
        verbose_name_plural = "Patrocinadores"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.nombre