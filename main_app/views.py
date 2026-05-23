from django.shortcuts import render

def home(request):
    # Django buscará automáticamente dentro de la carpeta 'templates'
    return render(request, 'main_app/home.html')