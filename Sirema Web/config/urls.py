from django.contrib.auth.decorators import login_not_required
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import include, path

from nucleo.views import inicio


@login_not_required
def favicon(request):
    return redirect(static("img/favicon.svg"), permanent=True)


urlpatterns = [
    path("", inicio, name="inicio"),
    path("favicon.ico", favicon),
    path("accesos/", include("accesos.urls")),
    path("inventario/", include("inventario.urls")),
    path("revisiones/", include("revisiones.urls")),
    path("reportes/", include("reportes.urls")),
]
