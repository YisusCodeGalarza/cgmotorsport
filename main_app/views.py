# views.py: El "Cerebro" de la aplicación.
# Recibe las peticiones desde urls.py, interactúa con models.py si necesita datos,
# y finalmente renderiza (dibuja) una plantilla HTML para enviarla al navegador.
from django.db.models import Q

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Patrocinador, Perfil, SeccionInteractiva, ComentarioSeccion, ComentarioPatrocinador, Album, Fotografia, ComentarioFoto, Evento, MensajeContacto, PropuestaPatrocinio, SuscripcionNewsletter
from .forms import LoginForm, RegistroForm, PerfilForm, EventoForm, PatrocinadorForm, AlbumForm, PropuestaForm, ContactoForm

# Función 'home': Es llamada por urls.py cuando alguien entra a la página principal.
def home(request):
    patrocinadores_activos = Patrocinador.objects.filter(es_activo=True)
    eventos_proximos = Evento.objects.filter(activo=True).order_by('fecha')[:3] # Traemos los próximos 3 eventos
    # render() toma la petición (request) y la une con el archivo HTML 'main_app/home.html'.
    # Se conecta con: El archivo main_app/templates/main_app/home.html.
    return render(request, 'main_app/home.html', {'patrocinadores': patrocinadores_activos, 'eventos': eventos_proximos})

# Función 'patrocinadores_view': Es llamada cuando se visita /patrocinadores/
def patrocinadores_view(request):
    if request.method == 'POST':
        # [MEJORA DE SEGURIDAD] Usamos el formulario para validar y limpiar los datos.
        form = PropuestaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Propuesta enviada! Nuestro equipo comercial la revisará y se pondrá en contacto pronto.")
            return redirect('patrocinadores')
        else:
            messages.error(request, "Hubo un error en el formulario. Por favor, revisa los datos.")
    else:
        form = PropuestaForm()
            
    patrocinadores_activos = Patrocinador.objects.filter(es_activo=True)
    # Pasamos el formulario a la plantilla para que lo renderice.
    # Nota: Deberás ajustar patrocinadores.html para renderizar los campos del formulario.
    # Se conecta con: El nuevo archivo patrocinadores.html que crearemos a continuación.
    return render(request, 'main_app/patrocinadores.html', {'patrocinadores': patrocinadores_activos, 'form': form})

# Función 'galeria_view': Muestra todos los álbumes y sus fotos/videos
def galeria_view(request):
    albumes_lista = Album.objects.prefetch_related('fotos__comentarios', 'fotos__likes').all()
    
    paginator = Paginator(albumes_lista, 10) # Muestra 10 álbumes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'main_app/galeria.html', {'albumes': page_obj, 'page_obj': page_obj})

# Función 'calendario_view': Es llamada cuando se visita /calendario/
def calendario_view(request):
    # Obtenemos todos los eventos activos y los ordenamos por fecha
    eventos = Evento.objects.filter(activo=True).order_by('fecha')

    # Capturamos los valores del formulario de búsqueda (si existen)
    query = request.GET.get('q')
    campeonato = request.GET.get('campeonato')
    sede = request.GET.get('sede')

    # Aplicamos los filtros al queryset de eventos
    if query:
        # Buscamos el texto en el nombre O en la descripción del evento
        # CORRECCIÓN: El campo se llama 'titulo', no 'nombre' en el modelo Evento.
        eventos = eventos.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))
    
    # if campeonato:
        # NOTA: Esta línea está comentada porque el campo 'campeonato' no existe en el modelo Evento.
        # Para que este filtro funcione, debes añadir el campo 'campeonato' a models.py y hacer una migración.
        # eventos = eventos.filter(campeonato__iexact=campeonato)

    if sede:
        # CORRECCIÓN: El campo se llama 'ubicacion', no 'sede' en el modelo Evento.
        eventos = eventos.filter(ubicacion__icontains=sede)

    context = {
        'eventos': eventos,
        'valores_busqueda': request.GET, # Devolvemos los valores para que el form los recuerde
    }
    # Se conecta con: El nuevo archivo calendario.html.
    return render(request, 'main_app/calendario.html', context)

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
    if request.method == 'POST':
        # [MEJORA DE SEGURIDAD] Usamos el formulario para validar y limpiar los datos.
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Gracias! Tu mensaje ha sido recibido exitosamente en nuestro panel.")
            return redirect('contacto')
        else:
            messages.error(request, "Hubo un error en el formulario. Por favor, revisa los datos.")
    else:
        form = ContactoForm()
            
    # Se conecta con: El nuevo archivo contacto.html.
    return render(request, 'main_app/contacto.html', {'form': form})

# NUEVA Función 'suscribir_newsletter'
def suscribir_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            SuscripcionNewsletter.objects.get_or_create(email=email)
            messages.success(request, "¡Te has suscrito al newsletter exitosamente!")
    # Redirige a la página desde la que se hizo el envío
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# Función 'login_view': Muestra el formulario de inicio de sesión
def login_view(request):
    # Si el usuario envió el formulario...
    if request.method == 'POST':
        # Pasamos los datos al formulario para que los inspeccione
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            # Intentamos autenticar
            # Django espera que el primer parámetro para la autenticación se llame 'username'.
            # Al renombrar el parámetro en la llamada a la función, Django sabe que debe buscar ese valor en el campo 'username' de la base de datos.
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido de vuelta al Paddock, {user.first_name or user.username}!")
                return redirect('home')
            else:
                # Este mensaje es más preciso, ya que el formulario era válido pero la autenticación falló.
                messages.error(request, "Credenciales incorrectas. Por favor, verifica tu correo y contraseña.")
        else:
            # Mostramos los errores específicos que detectó el formulario.
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
            
    # Se conecta con: El nuevo archivo login.html
    return render(request, 'main_app/login.html')

# Función 'registro_view': Muestra el formulario para crear cuenta nueva
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            # Creamos al usuario en la base de datos (Usamos el email como username porque debe ser único)
            user = User.objects.create_user(username=email, email=email, password=password, first_name=nombre)
            login(request, user)
            messages.success(request, f"¡Cuenta creada con éxito! Bienvenido al equipo, {nombre}.")
            return redirect('home')
        else:
            # Si hubo errores (ej: clave corta o correo repetido), se los mostramos al usuario
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, error)
            
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
        # Pasamos datos de texto (POST), imágenes (FILES) y le decimos quién es el usuario actual (user)
        form = PerfilForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('nombre')
            request.user.email = form.cleaned_data.get('email')
            request.user.username = form.cleaned_data.get('email')
            request.user.save()
            
            avatar = form.cleaned_data.get('avatar')
            if avatar:
                perfil.avatar = avatar
                perfil.save()
                
            messages.success(request, "¡Tu perfil ha sido actualizado con éxito!")
            return redirect('perfil')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, error)
        
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
def editar_comentario(request, id):
    comentario = get_object_or_404(ComentarioFoto, id=id)
    if request.method == 'POST' and request.user == comentario.usuario:
        nuevo_texto = request.POST.get('texto')
        if nuevo_texto:
            comentario.texto = nuevo_texto
            comentario.save()
            messages.success(request, "Comentario actualizado correctamente.")
    return redirect(f"{reverse('galeria')}?open={comentario.foto.id}")

@login_required(login_url='login')
def eliminar_comentario(request, id):
    comentario = get_object_or_404(ComentarioFoto, id=id)
    foto_id = comentario.foto.id
    if request.user == comentario.usuario:
        comentario.delete()
        messages.success(request, "Comentario eliminado.")
    return redirect(f"{reverse('galeria')}?open={foto_id}")

@login_required(login_url='login')
def reportar_comentario(request, id):
    comentario = get_object_or_404(ComentarioFoto, id=id)
    if request.method == 'POST':
        comentario.reportado = True
        comentario.save()
        messages.info(request, "El comentario ha sido reportado y será revisado por el equipo.")
    return redirect(f"{reverse('galeria')}?open={comentario.foto.id}")

# Vista para renderizar la página individual de foto_detalle.html (por si decides usarla de manera directa)
def foto_detalle_view(request, id):
    foto = get_object_or_404(Fotografia, id=id)
    return render(request, 'main_app/foto_detalle.html', {'foto': foto})

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

# ----------------------------------------------------------------------
# PANEL DE CONTROL PRIVADO (DASHBOARD)
# ----------------------------------------------------------------------

@staff_member_required(login_url='login')
def panel_home(request):
    stats = {
        'mensajes_noleidos': MensajeContacto.objects.filter(leido=False).count(),
        'propuestas_nuevas': PropuestaPatrocinio.objects.filter(revisado=False).count(),
        'eventos_activos': Evento.objects.filter(activo=True).count(),
        'patrocinadores': Patrocinador.objects.filter(es_activo=True).count(),
    }
    return render(request, 'main_app/panel_home.html', {'stats': stats})

@staff_member_required(login_url='login')
def panel_eventos(request):
    eventos = Evento.objects.all().order_by('-fecha')
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Carrera agregada exitosamente. Ya es visible en el calendario.")
            return redirect('panel_eventos')
    else:
        form = EventoForm()
    return render(request, 'main_app/panel_eventos.html', {'eventos': eventos, 'form': form})

@staff_member_required(login_url='login')
def panel_evento_editar(request, id):
    evento = get_object_or_404(Evento, id=id)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Carrera actualizada exitosamente.")
            return redirect('panel_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'main_app/panel_evento_editar.html', {'form': form, 'evento': evento})

@staff_member_required(login_url='login')
def panel_evento_eliminar(request, id):
    evento = get_object_or_404(Evento, id=id)
    evento.delete()
    messages.success(request, "Carrera eliminada del calendario.")
    return redirect('panel_eventos')

@staff_member_required(login_url='login')
def panel_patrocinadores(request):
    patrocinadores = Patrocinador.objects.all().order_by('-id')
    if request.method == 'POST':
        form = PatrocinadorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Patrocinador agregado exitosamente.")
            return redirect('panel_patrocinadores')
    else:
        form = PatrocinadorForm()
    return render(request, 'main_app/panel_patrocinadores.html', {'patrocinadores': patrocinadores, 'form': form})

@staff_member_required(login_url='login')
def panel_patrocinador_editar(request, id):
    patrocinador = get_object_or_404(Patrocinador, id=id)
    if request.method == 'POST':
        form = PatrocinadorForm(request.POST, request.FILES, instance=patrocinador)
        if form.is_valid():
            form.save()
            messages.success(request, "Patrocinador actualizado exitosamente.")
            return redirect('panel_patrocinadores')
    else:
        form = PatrocinadorForm(instance=patrocinador)
    return render(request, 'main_app/panel_patrocinador_editar.html', {'form': form, 'patrocinador': patrocinador})

@staff_member_required(login_url='login')
def panel_patrocinador_eliminar(request, id):
    patrocinador = get_object_or_404(Patrocinador, id=id)
    patrocinador.delete()
    messages.success(request, "Patrocinador eliminado.")
    return redirect('panel_patrocinadores')

@staff_member_required(login_url='login')
def panel_galeria(request):
    albumes = Album.objects.all().order_by('-fecha_creacion')
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Álbum creado exitosamente.")
            return redirect('panel_galeria')
    else:
        form = AlbumForm()
    return render(request, 'main_app/panel_galeria.html', {'albumes': albumes, 'form': form})

@staff_member_required(login_url='login')
def panel_album_editar(request, id):
    album = get_object_or_404(Album, id=id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, "Álbum actualizado exitosamente.")
            return redirect('panel_galeria')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'main_app/panel_album_editar.html', {'form': form, 'album': album})

@staff_member_required(login_url='login')
def panel_album_eliminar(request, id):
    album = get_object_or_404(Album, id=id)
    album.delete()
    messages.success(request, "Álbum eliminado por completo.")
    return redirect('panel_galeria')

@staff_member_required(login_url='login')
def panel_album_fotos(request, id):
    album = get_object_or_404(Album, id=id)
    if request.method == 'POST':
        archivos = request.FILES.getlist('fotos')
        
        subidos_count = 0
        for f in archivos:
            nombre_lower = f.name.lower()
            if nombre_lower.endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
                Fotografia.objects.create(
                    album=album,
                    archivo_video=f,
                    es_video=True
                )
            else:
                Fotografia.objects.create(
                    album=album,
                    imagen=f,
                    es_video=False
                )
            subidos_count += 1

        if subidos_count > 0:
            messages.success(request, f"Se subieron {subidos_count} archivo(s) exitosamente.")

        return redirect('panel_album_fotos', id=album.id)
    
    # CAMBIO AQUÍ: Forzar la consulta directa por el ID del álbum
    fotos = Fotografia.objects.filter(album=album).order_by('-id')
    return render(request, 'main_app/panel_album_fotos.html', {'album': album, 'fotos': fotos})

@staff_member_required(login_url='login')
def panel_foto_eliminar(request, id):
    foto = get_object_or_404(Fotografia, id=id)
    album_id = foto.album.id
    foto.delete()
    messages.success(request, "Archivo eliminado del álbum.")
    return redirect('panel_album_fotos', id=album_id)

@staff_member_required(login_url='login')
def panel_mensajes(request):
    mensajes = MensajeContacto.objects.all().order_by('-fecha_envio')
    return render(request, 'main_app/panel_mensajes.html', {'mensajes': mensajes})

@staff_member_required(login_url='login')
def panel_mensaje_leer(request, id):
    mensaje = get_object_or_404(MensajeContacto, id=id)
    mensaje.leido = not mensaje.leido
    mensaje.save()
    return redirect('panel_mensajes')

@staff_member_required(login_url='login')
def panel_mensaje_eliminar(request, id):
    mensaje = get_object_or_404(MensajeContacto, id=id)
    mensaje.delete()
    messages.success(request, "Mensaje eliminado.")
    return redirect('panel_mensajes')

@staff_member_required(login_url='login')
def panel_propuestas(request):
    propuestas = PropuestaPatrocinio.objects.all().order_by('-fecha_envio')
    return render(request, 'main_app/panel_propuestas.html', {'propuestas': propuestas})

@staff_member_required(login_url='login')
def panel_propuesta_revisar(request, id):
    propuesta = get_object_or_404(PropuestaPatrocinio, id=id)
    propuesta.revisado = not propuesta.revisado
    propuesta.save()
    return redirect('panel_propuestas')

@staff_member_required(login_url='login')
def panel_propuesta_eliminar(request, id):
    propuesta = get_object_or_404(PropuestaPatrocinio, id=id)
    propuesta.delete()
    messages.success(request, "Propuesta eliminada.")
    return redirect('panel_propuestas')

@staff_member_required(login_url='login')
def panel_suscriptores(request):
    suscriptores = SuscripcionNewsletter.objects.all()
    return render(request, 'main_app/panel_suscriptores.html', {'suscriptores': suscriptores})

@staff_member_required(login_url='login')
def panel_suscriptor_eliminar(request, id):
    suscriptor = get_object_or_404(SuscripcionNewsletter, id=id)
    suscriptor.delete()
    messages.success(request, "Suscriptor eliminado.")
    return redirect('panel_suscriptores')