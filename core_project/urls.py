"""
URL configuration for core_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

# 1. Rutas que NO llevan prefijo i18n
urlpatterns = [
    # Endpoint interno de Django para el cambio de idioma
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Forzar redirección directa de la raíz '/' a '/en/'
    path('', RedirectView.as_view(url='/en/', permanent=False)),
]

# 2. Rutas globales con prefijos de idioma (/en/ y /es/)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    prefix_default_language=True
)