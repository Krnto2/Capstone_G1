def permisos(request):
    usuario = getattr(request, "user", None)
    if usuario is None or not usuario.is_authenticated:
        return {"permisos": frozenset()}
    return {"permisos": usuario.permisos_codigos()}
