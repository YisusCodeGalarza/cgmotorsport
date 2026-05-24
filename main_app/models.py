# models.py: La "Base de Datos".
# Cada clase que hereda de models.Model se convierte en una tabla en tu base de datos.
# Se conecta con: admin.py (para gestionarlos) y views.py (para leerlos y enviarlos al HTML).

from django.db import models

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


# 2. MODELO PARA LA GALERÍA DE FOTOS (Aquí subirá sus tomas de acción)
class GaleriaFoto(models.Model):
    # ForeignKey es una relación de 1 a Muchos. Conecta esta foto con UN Evento específico.
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='fotos', null=True, blank=True, verbose_name="Evento Asociado")
    titulo = models.CharField(max_length=100, blank=True, verbose_name="Título de la foto")
    imagen = models.ImageField(upload_to='galeria/', verbose_name="Archivo de Imagen")
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foto de Galería"
        verbose_name_plural = "Galería de Fotos"

    def __str__(self):
        return self.titulo if self.titulo else f"Foto #{self.id}"


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

    class Meta:
        verbose_name = "Patrocinador"
        verbose_name_plural = "Patrocinadores"

    def __str__(self):
        return self.nombre