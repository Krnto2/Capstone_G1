from django import forms


class FormularioBootstrap:
    """Agrega las clases de Bootstrap 5 a los controles y marca los inválidos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            widget = campo.widget
            if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple, forms.RadioSelect)):
                clase = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                clase = "form-select"
            else:
                clase = "form-control"
            clases = widget.attrs.get("class", "")
            if clase not in clases:
                widget.attrs["class"] = f"{clases} {clase}".strip()

    def full_clean(self):
        super().full_clean()
        for nombre in self.errors:
            if nombre in self.fields:
                attrs = self.fields[nombre].widget.attrs
                if "is-invalid" not in attrs.get("class", ""):
                    attrs["class"] = f"{attrs.get('class', '')} is-invalid".strip()
                attrs["aria-invalid"] = "true"


class Formulario(FormularioBootstrap, forms.Form):
    pass


class FormularioModelo(FormularioBootstrap, forms.ModelForm):
    pass


class CampoFecha(forms.DateInput):
    input_type = "date"

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs, format="%Y-%m-%d")
