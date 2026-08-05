from django import forms
from django.contrib.auth.models import User
from .models import Evento, Patrocinador, Album, PropuestaPatrocinio, MensajeContacto

class LoginForm(forms.Form):
    # Validamos que sea un correo real y que ambos campos vengan con datos
    email = forms.EmailField(required=True, error_messages={'required': 'El correo es obligatorio.'})
    password = forms.CharField(required=True, error_messages={'required': 'La contraseña es obligatoria.'})

class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    # Exigimos seguridad básica en la contraseña
    password = forms.CharField(min_length=6, required=True, error_messages={'min_length': 'La contraseña debe tener al menos 6 caracteres.'})

    def clean_email(self):
        # Esta función revisa automáticamente si el correo ya existe en la base de datos
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Este correo ya está registrado. Por favor, inicia sesión.")
        return email

class PerfilForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    # La foto es opcional, y nos aseguramos de que sea realmente una imagen (Pillow la validará)
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Evitamos que cambie su correo por el de otro usuario que ya exista
        if self.user and User.objects.filter(username=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("Este correo ya está en uso por otra cuenta.")
        return email

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'fecha', 'ubicacion', 'descripcion', 'imagen', 'activo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-2 text-sm text-white focus:border-[#4781B3] outline-none'}),
            'titulo': forms.TextInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-2 text-sm text-white focus:border-[#4781B3] outline-none'}),
            'ubicacion': forms.TextInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-2 text-sm text-white focus:border-[#4781B3] outline-none'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-2 text-sm text-white focus:border-[#4781B3] outline-none', 'rows': 3}),
            'imagen': forms.FileInput(attrs={'class': 'text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-bold file:bg-[#4781B3] file:text-white cursor-pointer'}),
        }

class PatrocinadorForm(forms.ModelForm):
    class Meta:
        model = Patrocinador
        fields = ['nombre', 'logo', 'sitio_web', 'descripcion', 'es_activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-2 text-sm text-white focus:border-[#4781B3] outline-none'}),
            'sitio_web': forms.URLInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-2 text-sm text-white focus:border-[#4781B3] outline-none'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-2 text-sm text-white focus:border-[#4781B3] outline-none', 'rows': 3}),
            'logo': forms.FileInput(attrs={'class': 'text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-bold file:bg-[#4781B3] file:text-white cursor-pointer'}),
        }

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['titulo', 'descripcion', 'evento', 'portada']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-2 text-sm text-white focus:border-[#4781B3] outline-none'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-2 text-sm text-white focus:border-[#4781B3] outline-none', 'rows': 3}),
            'evento': forms.Select(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-2 text-sm text-gray-300 focus:border-[#4781B3] outline-none'}),
            'portada': forms.FileInput(attrs={'class': 'text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-bold file:bg-[#4781B3] file:text-white cursor-pointer'}),
        }

# [MEJORA DE SEGURIDAD] Formulario para validar y limpiar los datos de propuestas de patrocinio.
class PropuestaForm(forms.ModelForm):
    class Meta:
        model = PropuestaPatrocinio
        fields = ['nombre', 'puesto', 'email', 'telefono', 'organizacion', 'sitio_web', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
            'puesto': forms.TextInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
            'organizacion': forms.TextInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
            'sitio_web': forms.URLInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
            'mensaje': forms.Textarea(attrs={'rows': 3, 'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
        }

# [MEJORA DE SEGURIDAD] Formulario para validar y limpiar los datos del formulario de contacto.
class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'telefono', 'area_interes', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'First and Last Name(s)', 'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
            'email': forms.EmailInput(attrs={'placeholder': 'driver@example.com', 'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
            'asunto': forms.TextInput(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors'}),
            'mensaje': forms.Textarea(attrs={'rows': 4, 'placeholder': 'How can we help you?', 'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-white focus:border-[#4781B3] focus:outline-none transition-colors resize-none'}),
            'area_interes': forms.Select(attrs={'class': 'w-full bg-black/50 border border-white/10 rounded-lg p-3 text-sm text-gray-300 focus:border-[#4781B3] focus:outline-none transition-colors appearance-none cursor-pointer'},
                                         choices=[
                                             ('General', 'Información General'),
                                             ('Patrocinios', 'Patrocinios y Alianzas'),
                                             ('Prensa', 'Prensa y Medios'),
                                             ('Logistica', 'Logística del Equipo'),
                                         ])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que el widget de 'area_interes' use las opciones correctas
        self.fields['area_interes'].widget.choices = self.Meta.widgets['area_interes'].choices