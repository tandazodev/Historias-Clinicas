class DisableCSRFForAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)


class HealthCheckMiddleware:
    """Responde /health/ para el ALB antes de validar ALLOWED_HOSTS.

    El ALB consulta usando la IP privada de la instancia como Host, que no estaría en
    ALLOWED_HOSTS. Así se puede dejar ALLOWED_HOSTS restringido al DNS del ALB.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ('/health', '/health/'):
            from django.http import JsonResponse
            return JsonResponse({'status': 'ok'})
        return self.get_response(request)
