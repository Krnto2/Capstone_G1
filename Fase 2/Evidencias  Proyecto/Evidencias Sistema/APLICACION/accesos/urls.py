from django.urls import path

from . import views

app_name = "accesos"

urlpatterns = [
    path("ingresar/", views.IngresarView.as_view(), name="login"),
    path("salir/", views.SalirView.as_view(), name="logout"),
    path("perfil/", views.PerfilView.as_view(), name="perfil"),
    path("perfil/editar/", views.PerfilEditarView.as_view(), name="perfil_editar"),
    path("perfil/contrasena/", views.CambiarContrasenaView.as_view(), name="cambiar_contrasena"),
    path("perfil/foto/", views.FotoPerfilSubirView.as_view(), name="foto_perfil_subir"),
    path("perfil/foto/eliminar/", views.FotoPerfilEliminarView.as_view(), name="foto_perfil_eliminar"),
    path("usuarios/<int:pk>/foto/", views.FotoPerfilView.as_view(), name="foto_perfil"),
    path("usuarios/", views.UsuarioListaView.as_view(), name="usuarios"),
    path("usuarios/nuevo/", views.UsuarioCrearView.as_view(), name="usuario_crear"),
    path("usuarios/<int:pk>/editar/", views.UsuarioEditarView.as_view(), name="usuario_editar"),
    path("usuarios/<int:pk>/estado/", views.UsuarioEstadoView.as_view(), name="usuario_estado"),
    path("usuarios/<int:pk>/contrasena/", views.UsuarioContrasenaView.as_view(), name="usuario_contrasena"),
    path("permisos/", views.PermisosRolView.as_view(), name="permisos"),
    path("bitacora/", views.BitacoraView.as_view(), name="bitacora"),
    path("respaldos/", views.RespaldosView.as_view(), name="respaldos"),
    path("respaldos/nuevo/", views.RespaldoCrearView.as_view(), name="respaldo_crear"),
    path("respaldos/restaurar/", views.RespaldoRestaurarView.as_view(), name="respaldo_restaurar"),
    path("respaldos/<str:carpeta>/<str:nombre>/descargar/", views.RespaldoDescargarView.as_view(),
         name="respaldo_descargar"),
    path("respaldos/<str:carpeta>/<str:nombre>/eliminar/", views.RespaldoEliminarView.as_view(),
         name="respaldo_eliminar"),
]
