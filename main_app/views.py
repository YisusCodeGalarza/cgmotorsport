# views.py: El "Cerebro" de la aplicación.
# Recibe las peticiones desde urls.py, interactúa con models.py si necesita datos,
# y finalmente renderiza (dibuja) una plantilla HTML para enviarla al navegador.

from django.shortcuts import render
from .models import Patrocinador

# Función 'home': Es llamada por urls.py cuando alguien entra a la página principal.
def home(request):
    patrocinadores_activos = Patrocinador.objects.filter(es_activo=True)
    # render() toma la petición (request) y la une con el archivo HTML 'main_app/home.html'.
    # Se conecta con: El archivo main_app/templates/main_app/home.html.
    return render(request, 'main_app/home.html', {'patrocinadores': patrocinadores_activos})

# Función 'patrocinadores_view': Es llamada cuando se visita /patrocinadores/
def patrocinadores_view(request):
    patrocinadores_activos = Patrocinador.objects.filter(es_activo=True)
    # Se conecta con: El nuevo archivo patrocinadores.html que crearemos a continuación.
    return render(request, 'main_app/patrocinadores.html', {'patrocinadores': patrocinadores_activos})

# Función 'galeria_view': Es llamada cuando se visita /galeria/
def galeria_view(request):
    # Se conecta con: El nuevo archivo galeria.html.
    return render(request, 'main_app/galeria.html')

# Función 'calendario_view': Es llamada cuando se visita /calendario/
def calendario_view(request):
    # Se conecta con: El nuevo archivo calendario.html.
    return render(request, 'main_app/calendario.html')

# Función 'equipo_view': Es llamada cuando se visita /equipo/
def equipo_view(request):
    # Se conecta con: El nuevo archivo Team.html.
    return render(request, 'main_app/Team.html')

# Función 'todoterreno_view': Es llamada cuando se visita /todoterreno/
def todoterreno_view(request):
    # Se conecta con: El nuevo archivo todoterreno.html.
    return render(request, 'main_app/todoterreno.html')

# Función 'contacto_view': Es llamada cuando se visita /contacto/
def contacto_view(request):
    # Se conecta con: El nuevo archivo contacto.html.
    return render(request, 'main_app/contacto.html')

# Función 'login_view': Muestra el formulario de inicio de sesión
def login_view(request):
    # Se conecta con: El nuevo archivo login.html
    return render(request, 'main_app/login.html')

# Función 'registro_view': Muestra el formulario para crear cuenta nueva
def registro_view(request):
    # Se conecta con: El nuevo archivo registro.html
    return render(request, 'main_app/registro.html')