from django.shortcuts import redirect
from django.urls import reverse

EXEMPT_URLNAMES = ['login', 'logout', 'admin:login', 'admin:logout', 'admin:index']
EXEMPT_PATH_PREFIXES = ['/static/', '/media/', '/favicon.ico']


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Este se queda, pero ya no contiene la lógica
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):

        if any(request.path.startswith(prefix) for prefix in EXEMPT_PATH_PREFIXES):
            return None

        # Si el usuario ya está autenticado, permitir acceso
        if hasattr(request, 'user') and request.user.is_authenticated:
            return None

        # Si no hay URL resuelta o no está en la lista blanca, redirigir
        resolver_match = getattr(request, 'resolver_match', None)
        if resolver_match and resolver_match.url_name not in EXEMPT_URLNAMES:
            return redirect(reverse('usuarios:login'))

        return None
