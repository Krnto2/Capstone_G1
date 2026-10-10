from django.urls import path

from . import views

app_name = "reportes"

urlpatterns = [
    path("", views.ReportesView.as_view(), name="reportes"),
    path("panel/", views.PanelView.as_view(), name="panel"),
    path("exportar/<str:formato>/", views.ExportarView.as_view(), name="exportar"),
]
