# views.py: El "Cerebro" de la aplicación.
# Recibe las peticiones desde urls.py, interactúa con models.py si necesita datos,
# y finalmente renderiza (dibuja) una plantilla HTML para enviarla al navegador.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Patrocinador, Perfil, SeccionInteractiva, ComentarioSeccion, ComentarioPatrocinador, Album, Fotografia, ComentarioFoto, Evento

# Función 'home': Es llamada por urls.py cuando alguien entra a la página principal.
def home(request):
    patrocinadores_activos = Patrocinador.objects.filter(es_activo=True)
    eventos_proximos = Evento.objects.filter(activo=True).order_by('fecha')[:3] # Traemos los próximos 3 eventos
    # render() toma la petición (request) y la une con el archivo HTML 'main_app/home.html'.
    # Se conecta con: El archivo main_app/templates/main_app/home.html.
    return render(request, 'main_app/home.html', {'patrocinadores': patrocinadores_activos, 'eventos': eventos_proximos})

# Función 'patrocinadores_view': Es llamada cuando se visita /patrocinadores/
def patrocinadores_view(request):
    patrocinadores_activos = Patrocinador.objects.filter(es_activo=True)
    # Se conecta con: El nuevo archivo patrocinadores.html que crearemos a continuación.
    return render(request, 'main_app/patrocinadores.html', {'patrocinadores': patrocinadores_activos})

# Función 'galeria_view': Muestra todos los álbumes y sus fotos/videos
def galeria_view(request):
    albumes = Album.objects.prefetch_related('fotos__comentarios', 'fotos__likes').all()
    return render(request, 'main_app/galeria.html', {'albumes': albumes})

# Función 'calendario_view': Es llamada cuando se visita /calendario/
def calendario_view(request):
    # Se conecta con: El nuevo archivo calendario.html.
    return render(request, 'main_app/calendario.html')

# Función 'equipo_view': Es llamada cuando se visita /equipo/
def equipo_view(request):
    # Creamos o buscamos el registro para esta sección en particular
    seccion, _ = SeccionInteractiva.objects.get_or_create(nombre='equipo')
    return render(request, 'main_app/Team.html', {'seccion': seccion})

# Función 'todoterreno_view': Es llamada cuando se visita /todoterreno/
def todoterreno_view(request):
    seccion, _ = SeccionInteractiva.objects.get_or_create(nombre='todoterreno')
    return render(request, 'main_app/todoterreno.html', {'seccion': seccion})

# Función 'contacto_view': Es llamada cuando se visita /contacto/
def contacto_view(request):
    # Se conecta con: El nuevo archivo contacto.html.
    return render(request, 'main_app/contacto.html')

# Función 'login_view': Muestra el formulario de inicio de sesión
def login_view(request):
    # Si el usuario envió el formulario...
    if request.method == 'POST':
        # Obtenemos los datos (Asegúrate de que tus inputs en el HTML tengan estos atributos 'name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Django por defecto usa 'username' y 'password'. Como usaremos el correo, se lo pasamos al username.
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"¡Bienvenido de vuelta al Paddock, {user.first_name or user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Credenciales incorrectas. Verifica tu correo y contraseña.")
            
    # Se conecta con: El nuevo archivo login.html
    return render(request, 'main_app/login.html')

# Función 'registro_view': Muestra el formulario para crear cuenta nueva
def registro_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validar si el correo ya existe
        if User.objects.filter(username=email).exists():
            messages.error(request, "Este correo ya está registrado. Por favor, inicia sesión.")
        else:
            # Creamos al usuario en la base de datos (Usamos el email como username porque debe ser único)
            user = User.objects.create_user(username=email, email=email, password=password, first_name=nombre)
            # Lo iniciamos sesión automáticamente para que no tenga que volver a poner su clave
            login(request, user)
            messages.success(request, f"¡Cuenta creada con éxito! Bienvenido al equipo, {nombre}.")
            return redirect('home') # Lo enviamos a inicio temporalmente
            
    # Se conecta con: El nuevo archivo registro.html
    return render(request, 'main_app/registro.html')

# NUEVA Función 'logout_view': Para cerrar la sesión
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('home')

# NUEVA Función 'perfil_view': Permite al usuario editar su cuenta y subir su foto
@login_required(login_url='login')
def perfil_view(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        avatar = request.FILES.get('avatar') # Usamos request.FILES para las imágenes
        
        request.user.first_name = nombre
        request.user.email = email
        request.user.username = email
        request.user.save()
        
        if avatar:
            perfil.avatar = avatar
            perfil.save()
            
        messages.success(request, "¡Tu perfil ha sido actualizado con éxito!")
        return redirect('perfil')
        
    return render(request, 'main_app/Usuarios.html', {'perfil': perfil})

# ----------------------------------------------------------------------
# LÓGICAS INTERACTIVAS (LIKES Y COMENTARIOS PARA PATROCINADORES Y SECCIONES)
# ----------------------------------------------------------------------

@login_required(login_url='login')
def like_foto(request, id):
    foto = get_object_or_404(Fotografia, id=id)
    if request.user in foto.likes.all():
        foto.likes.remove(request.user)
    else:
        foto.likes.add(request.user)
    # Al terminar, lo regresamos a la galería indicando que reabra esa foto específica
    return redirect(f"{reverse('galeria')}?open={foto.id}")

@login_required(login_url='login')
def comentar_foto(request, id):
    foto = get_object_or_404(Fotografia, id=id)
    if request.method == 'POST' and request.POST.get('comentario'):
        ComentarioFoto.objects.create(foto=foto, usuario=request.user, texto=request.POST.get('comentario'))
    return redirect(f"{reverse('galeria')}?open={foto.id}")

@login_required(login_url='login')
def like_patrocinador(request, id):
    patrocinador = get_object_or_404(Patrocinador, id=id)
    if request.user in patrocinador.likes.all():
        patrocinador.likes.remove(request.user)
    else:
        patrocinador.likes.add(request.user)
    return redirect(f"{reverse('patrocinadores')}#patrocinador-{id}")

@login_required(login_url='login')
def comentar_patrocinador(request, id):
    patrocinador = get_object_or_404(Patrocinador, id=id)
    if request.method == 'POST' and request.POST.get('comentario'):
        ComentarioPatrocinador.objects.create(patrocinador=patrocinador, usuario=request.user, texto=request.POST.get('comentario'))
        messages.success(request, "Comentario añadido.")
    return redirect(f"{reverse('patrocinadores')}#patrocinador-{id}")

@login_required(login_url='login')
def eliminar_comentario_patrocinador(request, id):
    comentario = get_object_or_404(ComentarioPatrocinador, id=id)
    if comentario.usuario == request.user:
        comentario.delete()
    return redirect(f"{reverse('patrocinadores')}#patrocinador-{comentario.patrocinador.id}")

@login_required(login_url='login')
def like_seccion(request, nombre):
    seccion, _ = SeccionInteractiva.objects.get_or_create(nombre=nombre)
    if request.user in seccion.likes.all():
        seccion.likes.remove(request.user)
    else:
        seccion.likes.add(request.user)
    return redirect(nombre)

@login_required(login_url='login')
def comentar_seccion(request, nombre):
    seccion, _ = SeccionInteractiva.objects.get_or_create(nombre=nombre)
    if request.method == 'POST' and request.POST.get('comentario'):
        ComentarioSeccion.objects.create(seccion=seccion, usuario=request.user, texto=request.POST.get('comentario'))
    return redirect(nombre)

@login_required(login_url='login')
def eliminar_comentario_seccion(request, id):
    comentario = get_object_or_404(ComentarioSeccion, id=id)
    if comentario.usuario == request.user:
        comentario.delete()
    return redirect(comentario.seccion.nombre)