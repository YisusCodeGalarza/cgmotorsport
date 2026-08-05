# main_app/middleware.py
from django.shortcuts import redirect

class ForceDefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si el usuario entra a la raíz '/' exacta y no ha elegido idioma explícitamente en cookies
        if request.path == '/' and 'django_language' not in request.COOKIES:
            return redirect('/en/')
        return self.get_response(request)