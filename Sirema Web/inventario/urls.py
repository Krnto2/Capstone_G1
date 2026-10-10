from django.urls import path

from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.MaterialListaView.as_view(), name="lista"),
    path("nuevo/", views.MaterialCrearView.as_view(), name="crear"),
    path("importar/", views.ImportarView.as_view(), name="importar"),
    path("importar/plantilla.csv", views.PlantillaImportacionView.as_view(), name="plantilla"),
    path("<int:pk>/", views.MaterialDetalleView.as_view(), name="detalle"),
    path("<int:pk>/editar/", views.MaterialEditarView.as_view(), name="editar"),
    path("<int:pk>/baja/", views.MaterialBajaView.as_view(), name="baja"),
    path("<int:pk>/trasladar/", views.MovimientoView.as_view(), name="trasladar"),
    path("unidades/", views.UnidadesView.as_view(), name="unidades"),
    path("unidades/nueva/", views.UnidadFormView.as_view(), name="unidad_crear"),
    path("unidades/<int:pk>/editar/", views.UnidadFormView.as_view(), name="unidad_editar"),
    path("cajoneras/nueva/", views.CajoneraFormView.as_view(), name="cajonera_crear"),
    path("cajoneras/<int:pk>/editar/", views.CajoneraFormView.as_view(), name="cajonera_editar"),
    path("categorias/", views.CategoriasView.as_view(), name="categorias"),
    path("categorias/nueva/", views.CategoriaFormView.as_view(), name="categoria_crear"),
    path("categorias/<int:pk>/editar/", views.CategoriaFormView.as_view(), name="categoria_editar"),
    path("<str:entidad>/<int:pk>/eliminar/", views.EliminarCatalogoView.as_view(), name="eliminar"),
]
