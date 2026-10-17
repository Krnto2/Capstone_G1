from django import forms
from django.core.exceptions import ValidationError

from nucleo.enums import EstadoMaterial, TipoMaterial
from nucleo.formularios import Formulario, FormularioModelo
from nucleo.utilidades import normalizar_codigo

from . import services
from .models import Cajonera, Categoria, Material, Unidad


def opciones_cajoneras(solo_activas=True):
    """Cajoneras agrupadas por unidad para un <select> con <optgroup>."""
    cajoneras = Cajonera.objects.select_related("unidad")
    if solo_activas:
        cajoneras = cajoneras.filter(unidad__activo=True)
    grupos = {}
    for cajonera in cajoneras:
        grupos.setdefault(str(cajonera.unidad), []).append((cajonera.pk, cajonera.nombre))
    return [("", "Seleccione…")] + list(grupos.items())


class CampoCajonera(forms.ModelChoiceField):
    """Las opciones agrupadas se cargan en el __init__ de cada formulario."""

    def __init__(self, **kwargs):
        super().__init__(queryset=Cajonera.objects.select_related("unidad"), **kwargs)

    def label_from_instance(self, obj):
        return str(obj)


class FormularioMaterial(FormularioModelo):
    """CU-B1 Registrar material y CU-B2 Modificar ficha."""

    cajonera = CampoCajonera(label="Ubicación (unidad / cajonera)")

    class Meta:
        model = Material
        fields = ["codigo_institucional", "nombre", "categoria", "cajonera", "tipo", "cantidad",
                  "marca", "modelo", "numero_serie", "observaciones"]
        widgets = {
            "codigo_institucional": forms.TextInput(attrs={"placeholder": "8C-0112", "autocomplete": "off",
                                                           "class": "text-uppercase"}),
            "observaciones": forms.Textarea(attrs={"rows": 2}),
            "cantidad": forms.NumberInput(attrs={"min": 1, "inputmode": "numeric"}),
        }
        help_texts = {
            "codigo_institucional": "Obligatorio para el material unitario. No distingue mayúsculas.",
            "numero_serie": "Opcional: no identifica al elemento.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].empty_label = "Seleccione…"
        self.fields["cajonera"].widget.choices = opciones_cajoneras()
        if self.instance.pk:
            # La ubicación de un elemento existente solo cambia con un movimiento (RF-06).
            del self.fields["cajonera"]

    def clean_codigo_institucional(self):
        codigo = normalizar_codigo(self.cleaned_data.get("codigo_institucional"))
        return services.verificar_codigo(codigo, excluir_pk=self.instance.pk)

    def clean(self):
        datos = super().clean()
        if datos.get("tipo") == TipoMaterial.UNITARIO:
            if not datos.get("codigo_institucional") and "codigo_institucional" not in self.errors:
                self.add_error("codigo_institucional",
                               "El código institucional es obligatorio para el material unitario.")
            datos["cantidad"] = 1
        return datos


class FiltroMaterial(Formulario):
    """RF-05: búsqueda por nombre o código y filtros combinados."""

    es_filtro = True

    q = forms.CharField(label="Buscar", required=False,
                        widget=forms.SearchInput(attrs={"placeholder": "Nombre o código (desde 2 caracteres)",
                                                        "autocomplete": "off"}))
    unidad = forms.ModelChoiceField(label="Unidad", queryset=Unidad.objects.all(), required=False,
                                    empty_label="Todas")
    cajonera = CampoCajonera(label="Cajonera", required=False)
    categoria = forms.ModelChoiceField(label="Categoría", queryset=Categoria.objects.all(), required=False,
                                       empty_label="Todas")
    estado = forms.ChoiceField(label="Estado", required=False,
                               choices=[("activo", "Activos"), ("de_baja", "Dados de baja"), ("todos", "Todos")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cajonera"].widget.choices = [("", "Todas")] + opciones_cajoneras(False)[1:]

    def filtrar(self, materiales):
        if not self.is_valid():
            return materiales.activos()
        datos = self.cleaned_data
        estado = datos.get("estado") or "activo"
        if estado in EstadoMaterial.values:
            materiales = materiales.filter(estado=estado)
        materiales = materiales.buscar(datos.get("q"))
        if datos.get("unidad"):
            materiales = materiales.filter(cajonera__unidad=datos["unidad"])
        if datos.get("cajonera"):
            materiales = materiales.filter(cajonera=datos["cajonera"])
        if datos.get("categoria"):
            materiales = materiales.filter(categoria=datos["categoria"])
        return materiales


class FormularioMovimiento(Formulario):
    """CU-B5 Registrar movimiento de material."""

    cajonera_destino = CampoCajonera(label="Nueva ubicación")
    motivo = forms.CharField(label="Motivo", max_length=200, required=False,
                             widget=forms.TextInput(attrs={"placeholder": "Ej.: reorganización de la cabina"}))

    def __init__(self, *args, material=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.material = material
        self.fields["cajonera_destino"].widget.choices = opciones_cajoneras()

    def clean_cajonera_destino(self):
        destino = self.cleaned_data["cajonera_destino"]
        if self.material and destino.pk == self.material.cajonera_id:
            raise ValidationError("El elemento ya se encuentra en esa ubicación.")
        return destino


class FormularioBaja(Formulario):
    """CU-B3 Dar de baja material."""

    motivo = forms.CharField(label="Motivo de la baja", max_length=200,
                             widget=forms.TextInput(attrs={"placeholder": "Ej.: roto en emergencia"}))
    destino_final = forms.CharField(label="Destino final", max_length=100, required=False)
    confirmar = forms.BooleanField(
        label="Entiendo que la baja cierra sus planes y deja no realizadas sus revisiones pendientes.")


class FormularioImportacion(Formulario):
    archivo = forms.FileField(label="Planilla CSV o XLSX",
                              widget=forms.ClearableFileInput(attrs={"accept": ".csv,.xlsx"}))


class FormularioUnidad(FormularioModelo):
    class Meta:
        model = Unidad
        fields = ["codigo", "nombre", "tipo", "activo"]
        widgets = {"codigo": forms.TextInput(attrs={"placeholder": "B-8", "class": "text-uppercase"})}

    def clean_codigo(self):
        codigo = normalizar_codigo(self.cleaned_data["codigo"])
        if Unidad.objects.filter(codigo__iexact=codigo).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ya existe una unidad con ese código.")
        return codigo


class FormularioCajonera(FormularioModelo):
    class Meta:
        model = Cajonera
        fields = ["unidad", "nombre", "descripcion", "orden"]

    def clean(self):
        datos = super().clean()
        unidad, nombre = datos.get("unidad"), (datos.get("nombre") or "").strip()
        if unidad and nombre and Cajonera.objects.filter(unidad=unidad, nombre__iexact=nombre)\
                .exclude(pk=self.instance.pk).exists():
            self.add_error("nombre", "Ya existe una cajonera con ese nombre en la unidad.")
        return datos


class FormularioCategoria(FormularioModelo):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip().upper()
        if Categoria.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ya existe una categoría con ese nombre.")
        return nombre
