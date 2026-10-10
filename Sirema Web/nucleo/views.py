from django.shortcuts import redirect


def inicio(request):
    """Página de inicio según el rol: panel para la jefatura, revisiones para el resto."""
    usuario = request.user
    if usuario.tiene_permiso("panel.consultar"):
        return redirect("reportes:panel")
    if usuario.tiene_permiso("revision.ejecutar"):
        return redirect("revisiones:mis_revisiones")
    if usuario.tiene_permiso("usuario.administrar"):
        return redirect("accesos:usuarios")
    return redirect("inventario:lista")
