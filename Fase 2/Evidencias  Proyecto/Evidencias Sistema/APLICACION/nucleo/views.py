from django.shortcuts import redirect


def inicio(request):
    usuario = request.user
    if usuario.tiene_permiso("panel.consultar"):
        return redirect("reportes:panel")
    if usuario.tiene_permiso("revision.ejecutar"):
        return redirect("revisiones:mis_revisiones")
    if usuario.tiene_permiso("usuario.administrar"):
        return redirect("accesos:usuarios")
    return redirect("inventario:lista")
