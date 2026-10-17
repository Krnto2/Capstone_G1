from django import forms
from django.core.exceptions import ValidationError

from accesos.models import Usuario
from inventario.models import Unidad
from nucleo.enums import CriticidadHallazgo, EstadoHallazgo, EstadoRevision, TipoDatoPunto
from nucleo.formularios import CampoFecha, Formulario, FormularioModelo
from nucleo.utilidades import hoy

from .models import PlanRevision


def responsables():
    return Usuario.objects.con_permiso("revision.ejecutar").order_by("apellidos", "nombre")


class CampoUsuario(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nombre_completo} · {obj.rol}"


class FormularioPlan(FormularioModelo):
    """CU-C1 Definir plan de revisión."""

    class Meta:
        model = PlanRevision
        fields = ["nombre", "descripcion", "frecuencia_valor", "frecuencia_unidad", "dias_tolerancia",
                  "exige_fotografia"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 2, "placeholder": "Indicaciones del fabricante o del "
                                                                           "procedimiento, visibles al ejecutar."}),
            "frecuencia_valor": forms.NumberInput(attrs={"min": 1, "inputmode": "numeric"}),
            "dias_tolerancia": forms.NumberInput(attrs={"min": 0, "inputmode": "numeric"}),
        }
        help_texts = {
            "dias_tolerancia": "Días después de la fecha programada antes de quedar vencida.",
            "exige_fotografia": "La revisión no se finaliza sin al menos una fotografía.",
        }

    def validate_unique(self):
        # La versión se asigna en el servicio, que mantiene único (nombre, versión).
        pass


class FormularioPunto(Formulario):
    """CU-C2 Definir puntos de control."""

    descripcion = forms.CharField(label="Acción a verificar", max_length=200,
                                  widget=forms.TextInput(attrs={"placeholder": "Ej.: Lectura de CO en aire limpio"}))
    tipo_dato = forms.ChoiceField(label="Tipo", choices=TipoDatoPunto.choices, initial=TipoDatoPunto.BOOLEANO)
    unidad_medida = forms.CharField(label="Unidad", max_length=15, required=False,
                                    widget=forms.TextInput(attrs={"placeholder": "ppm"}))
    valor_minimo = forms.DecimalField(label="Mínimo", max_digits=10, decimal_places=2, required=False,
                                      widget=forms.NumberInput(attrs={"step": "any", "inputmode": "decimal"}))
    valor_maximo = forms.DecimalField(label="Máximo", max_digits=10, decimal_places=2, required=False,
                                      widget=forms.NumberInput(attrs={"step": "any", "inputmode": "decimal"}))
    obligatorio = forms.BooleanField(label="Obligatorio", required=False, initial=True)
    exige_fotografia = forms.BooleanField(label="Exige foto", required=False)

    def clean(self):
        datos = super().clean()
        if datos.get("tipo_dato") != TipoDatoPunto.NUMERICO:
            datos["valor_minimo"] = datos["valor_maximo"] = None
            datos["unidad_medida"] = None
        minimo, maximo = datos.get("valor_minimo"), datos.get("valor_maximo")
        if minimo is not None and maximo is not None and maximo < minimo:
            self.add_error("valor_maximo", "El máximo no puede ser menor que el mínimo.")
        datos["unidad_medida"] = (datos.get("unidad_medida") or "").strip() or None
        return datos


class BaseFormsetPuntos(forms.BaseFormSet):
    default_error_messages = {**forms.BaseFormSet.default_error_messages,
                              "too_few_forms": "El plan debe tener al menos un punto de control."}

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        vigentes = [f for f in self.forms if f.cleaned_data and not self._should_delete_form(f)]
        if not vigentes:
            raise ValidationError("El plan debe tener al menos un punto de control.")

    def puntos(self):
        vigentes = [f for f in self.ordered_forms if f.cleaned_data] if self.can_order else self.forms
        return [f.cleaned_data for f in vigentes if f.cleaned_data and not self._should_delete_form(f)]


FormsetPuntos = forms.formset_factory(FormularioPunto, formset=BaseFormsetPuntos, extra=0, can_delete=True,
                                      can_order=True, min_num=1, validate_min=True)


class FormularioAsignacion(Formulario):
    """CU-C3 Asignar plan a material (el elemento se elige tras buscarlo)."""

    plan = forms.ModelChoiceField(label="Plan de revisión", queryset=PlanRevision.objects.none(),
                                  empty_label="Seleccione…")
    responsable = CampoUsuario(label="Bombero responsable", queryset=Usuario.objects.none(),
                               empty_label="Seleccione…")
    fecha_inicio = forms.DateField(label="Fecha de la primera revisión", widget=CampoFecha())
    fecha_termino = forms.DateField(label="Fecha de término", required=False, widget=CampoFecha())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["plan"].queryset = PlanRevision.objects.filter(activo=True, puntos__isnull=False).distinct()
        self.fields["responsable"].queryset = responsables()
        self.fields["fecha_inicio"].initial = hoy()

    def clean_fecha_inicio(self):
        fecha = self.cleaned_data["fecha_inicio"]
        if fecha < hoy():
            raise ValidationError("La primera revisión no puede quedar en una fecha pasada.")
        return fecha

    def clean(self):
        datos = super().clean()
        inicio, termino = datos.get("fecha_inicio"), datos.get("fecha_termino")
        if inicio and termino and termino < inicio:
            self.add_error("fecha_termino", "La fecha de término no puede ser anterior a la de inicio.")
        return datos


class FormularioFinalizar(Formulario):
    """CU-C7 paso 5 y CU-C12 Registrar hallazgo (pantalla M4)."""

    observaciones = forms.CharField(label="Observaciones generales", max_length=500, required=False,
                                    widget=forms.Textarea(attrs={"rows": 2}))
    descripcion = forms.CharField(label="Descripción del hallazgo", max_length=500, required=False,
                                  widget=forms.Textarea(attrs={"rows": 4, "placeholder":
                                                               "Qué falla, qué se hizo con el equipo…"}))
    criticidad = forms.ChoiceField(label="Criticidad", choices=CriticidadHallazgo.choices, required=False,
                                   widget=forms.RadioSelect)

    def __init__(self, *args, requiere_hallazgo=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.requiere_hallazgo = requiere_hallazgo
        self.fields["descripcion"].required = requiere_hallazgo
        self.fields["criticidad"].required = requiere_hallazgo
        self.fields["descripcion"].error_messages["required"] = ("Una revisión con falla no se finaliza sin "
                                                                 "describir el hallazgo.")
        self.fields["criticidad"].error_messages["required"] = "Seleccione la criticidad."


class FormularioMotivo(Formulario):
    motivo = forms.CharField(label="Motivo de la anulación", max_length=300,
                             widget=forms.Textarea(attrs={"rows": 3}))


class FormularioCierreHallazgo(Formulario):
    acciones = forms.CharField(label="Acción tomada", max_length=500,
                               widget=forms.Textarea(attrs={"rows": 3, "placeholder":
                                                            "Ej.: sensor reemplazado y equipo calibrado por el "
                                                            "servicio técnico."}))


class FormularioReasignar(Formulario):
    responsable = CampoUsuario(label="Nuevo responsable", queryset=Usuario.objects.none(), empty_label="Seleccione…")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["responsable"].queryset = responsables()


class FiltroRevisiones(Formulario):
    es_filtro = True

    q = forms.CharField(label="Elemento", required=False,
                        widget=forms.SearchInput(attrs={"placeholder": "Nombre o código"}))
    estado = forms.ChoiceField(label="Estado", required=False, choices=[("", "Todos")] + list(EstadoRevision.choices))
    unidad = forms.ModelChoiceField(label="Unidad", queryset=Unidad.objects.all(), required=False,
                                    empty_label="Todas")
    responsable = CampoUsuario(label="Responsable", queryset=Usuario.objects.none(), required=False,
                               empty_label="Todos")
    desde = forms.DateField(label="Límite desde", required=False, widget=CampoFecha())
    hasta = forms.DateField(label="Límite hasta", required=False, widget=CampoFecha())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["responsable"].queryset = Usuario.objects.personas()


class FiltroHallazgos(Formulario):
    es_filtro = True

    estado = forms.ChoiceField(label="Estado", required=False,
                               choices=[("abiertos", "Abiertos y en reparación")] + list(EstadoHallazgo.choices)
                               + [("todos", "Todos")])
    criticidad = forms.ChoiceField(label="Criticidad", required=False,
                                   choices=[("", "Todas")] + list(CriticidadHallazgo.choices))
