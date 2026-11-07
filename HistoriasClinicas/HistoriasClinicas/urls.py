from django.contrib import admin
from django.http import JsonResponse
from django.conf import settings
from django.urls import include, path, re_path
from django.http import FileResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
def api_root(request):
    """Vista raíz de la API"""
    return JsonResponse({
        "success": True,
        "message": "API HistoriasClinicas v1",
        "endpoints": {
            "admin": "/admin/",
            "Historias": "/api/v1/historias/",
            "documentacion_historias": {
                "historias_clinicas": "/api/v1/historias/historias-clinicas/",
                "casos": "/api/v1/historias/casos/",
                "antecedentes": "/api/v1/historias/antecedentes/",
                "documentos": "/api/v1/historias/documentos/"
            },
            "agendas": "/api/v1/agendas/",
            "notificaciones": "/api/v1/notificaciones/",
            "auth": "/api/v1/auth/",
            "reportes": "/api/v1/reportes/",
            "documentacion": {
                "atenciones": "/api/v1/reportes/atenciones/",
                "estadisticas": "/api/v1/reportes/estadisticas/",
                "consultas_por_genero": "/api/v1/reportes/consultas-por-genero/",
                "diagnosticos_frecuentes": "/api/v1/reportes/diagnosticos-frecuentes/",
                "servicios_mas_usados": "/api/v1/reportes/servicios-mas-usados/",
            }
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),

    path('api/v1/agendas/', include('Agendas.urls')),
    path('api/v1/auth/', include('Seguridad.urls')),
    path('api/v1/historias/', include('Historias.urls')),
    path('api/v1/reportes/', include('Reportes.urls')),
    path('api/v1/notificaciones/', include('Notificaciones.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair_v1'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_v1'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# El front llama a /backend/api/... (en Docker lo reescribe nginx). En AWS no hay nginx:
# se acepta el mismo prefijo aquí.
urlpatterns += [path('backend/', include([
    path('', api_root),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]))]

# SPA: cualquier ruta que no sea API/admin/static devuelve index.html del front compilado.
_index = getattr(settings, 'FRONTEND_DIST', None) and (settings.FRONTEND_DIST / 'index.html')
if _index and _index.exists():
    def spa_index(request, *args, **kwargs):
        return FileResponse(open(_index, 'rb'), content_type='text/html; charset=utf-8')

    urlpatterns += [re_path(r'^(?!api/|admin/|static/|media/|backend/|health).*$', spa_index)]
