from django.urls import path

from . import api, views

app_name = "revisiones"

urlpatterns = [
    path("", views.MisRevisionesView.as_view(), name="mis_revisiones"),
    path("todas/", views.RevisionListaView.as_view(), name="lista"),
    path("<int:pk>/", views.RevisionDetalleView.as_view(), name="detalle"),
    path("<int:pk>/ejecutar/", views.EjecutarView.as_view(), name="ejecutar"),
    path("<int:pk>/finalizar/", views.FinalizarView.as_view(), name="finalizar"),
    path("<int:pk>/reasignar/", views.ReasignarView.as_view(), name="reasignar"),
    path("fotografias/<uuid:pk>/", views.FotografiaView.as_view(), name="fotografia"),
    path("fotografias/<uuid:pk>/anular/", views.AnularFotografiaView.as_view(), name="anular_foto"),
    path("planes/", views.PlanListaView.as_view(), name="planes"),
    path("planes/nuevo/", views.PlanFormView.as_view(), name="plan_crear"),
    path("planes/<int:pk>/", views.PlanDetalleView.as_view(), name="plan"),
    path("planes/<int:pk>/editar/", views.PlanFormView.as_view(), name="plan_editar"),
    path("planes/<int:pk>/desactivar/", views.PlanDesactivarView.as_view(), name="plan_desactivar"),
    path("asignaciones/", views.AsignacionListaView.as_view(), name="asignaciones"),
    path("asignaciones/nueva/", views.AsignacionCrearView.as_view(), name="asignacion_crear"),
    path("asignaciones/<int:pk>/cerrar/", views.AsignacionCerrarView.as_view(), name="asignacion_cerrar"),
    path("hallazgos/", views.HallazgoListaView.as_view(), name="hallazgos"),
    path("hallazgos/<int:pk>/", views.HallazgoDetalleView.as_view(), name="hallazgo"),
    path("notificaciones/", views.NotificacionListaView.as_view(), name="notificaciones"),
    path("notificaciones/<int:pk>/", views.NotificacionAbrirView.as_view(), name="notificacion"),
    path("notificaciones/leer-todas/", views.MarcarTodasLeidasView.as_view(), name="leer_todas"),
    # API JSON de ejecución (autoguardado y fotografías)
    path("api/revisiones/<int:pk>/puntos/<int:punto_id>/", api.registrar_punto, name="api_punto"),
    path("api/revisiones/<int:pk>/fotografias/", api.subir_fotografia, name="api_fotografia"),
    path("api/revisiones/<int:pk>/estado/", api.estado_revision, name="api_estado"),
]
