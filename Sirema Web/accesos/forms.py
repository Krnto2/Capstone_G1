from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm

from nucleo.enums import AccionAuditoria
from nucleo.formularios import CampoFecha, Formulario, FormularioBootstrap, FormularioModelo
from nucleo.utilidades import formatear_rut, rut_valido

from .models import Rol, Usuario


class FormularioIngreso(FormularioBootstrap, AuthenticationForm):
    username = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={"autocomplete": "email", "autofocus": True,
                                       "placeholder": "nombre@ejemplo.cl", "inputmode": "email"}),
    )
    password = forms.CharField(
        label="Contraseña", strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages = {
        "invalid_login": "Correo o contraseña incorrectos. Tras 5 intentos fallidos la cuenta "
                         "se bloquea por 15 minutos.",
        "inactive": "Esta cuenta está desactivada. Consulte al administrador de la compañía.",
    }


class FormularioCambioContrasena(FormularioBootstrap, PasswordChangeForm):
    """CU-A2: el cambio exige la contraseña actual (RF-02)."""


class FormularioRestablecerContrasena(FormularioBootstrap, SetPasswordForm):
    """El administrador asigna una contraseña nueva (no hay recuperación por correo)."""


class FormularioUsuario(FormularioModelo):
    contrasena1 = forms.CharField(label="Contraseña inicial", strip=False, widget=forms.PasswordInput,
                                  help_text=password_validation.password_validators_help_text_html())
    contrasena2 = forms.CharField(label="Repita la contraseña", strip=False, widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ["rut", "nombre", "apellidos", "correo", "telefono", "rol"]
        widgets = {
            "rut": forms.TextInput(attrs={"placeholder": "12.345.678-9", "autocomplete": "off"}),
            "telefono": forms.TextInput(attrs={"placeholder": "+56 9 1234 5678", "inputmode": "tel"}),
            "correo": forms.EmailInput(attrs={"inputmode": "email"}),
        }
        error_messages = {
            "rut": {"unique": "Ya existe un usuario con este RUT."},
            "correo": {"unique": "Ya existe un usuario con este correo."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rol"].queryset = Rol.objects.filter(activo=True)
        self.fields["rol"].empty_label = None
        if self.instance.pk:
            del self.fields["contrasena1"]
            del self.fields["contrasena2"]

    def clean_rut(self):
        rut = self.cleaned_data["rut"]
        if not rut_valido(rut):
            raise forms.ValidationError("El RUT no es válido. Revise el dígito verificador.")
        return formatear_rut(rut)

    def clean_correo(self):
        correo = self.cleaned_data["correo"].strip().lower()
        existentes = Usuario.objects.filter(correo__iexact=correo).exclude(pk=self.instance.pk)
        if existentes.exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        return correo

    def clean_rol(self):
        rol = self.cleaned_data["rol"]
        if self.instance.pk and rol.nombre != Rol.ADMINISTRADOR:
            original = Usuario.objects.get(pk=self.instance.pk)
            if original.es_unico_administrador_activo():
                raise forms.ValidationError("No se puede quitar el rol al único administrador activo.")
        return rol

    def clean(self):
        datos = super().clean()
        c1, c2 = datos.get("contrasena1"), datos.get("contrasena2")
        if "contrasena1" in self.fields and c1:
            if c1 != c2:
                self.add_error("contrasena2", "Las contraseñas no coinciden.")
            else:
                usuario = Usuario(rut=datos.get("rut", ""), nombre=datos.get("nombre", ""),
                                  apellidos=datos.get("apellidos", ""), correo=datos.get("correo", ""))
                try:
                    password_validation.validate_password(c1, usuario)
                except forms.ValidationError as error:
                    self.add_error("contrasena1", error)
        return datos

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if "contrasena1" in self.fields:
            usuario.set_password(self.cleaned_data["contrasena1"])
        if commit:
            usuario.save()
        return usuario


class FiltroUsuarios(Formulario):
    q = forms.CharField(label="Buscar", required=False,
                        widget=forms.TextInput(attrs={"placeholder": "Nombre, RUT o correo"}))
    rol = forms.ModelChoiceField(label="Rol", queryset=Rol.objects.all(), required=False, empty_label="Todos")
    estado = forms.ChoiceField(label="Estado", required=False,
                               choices=[("", "Todos"), ("activo", "Activos"), ("inactivo", "Desactivados")])


class FiltroBitacora(Formulario):
    usuario = forms.ModelChoiceField(label="Usuario", required=False, empty_label="Todos",
                                     queryset=Usuario.objects.all())
    accion = forms.ChoiceField(label="Acción", required=False,
                               choices=[("", "Todas")] + list(AccionAuditoria.choices))
    entidad = forms.CharField(label="Entidad", required=False,
                              widget=forms.TextInput(attrs={"placeholder": "material, revision…"}))
    desde = forms.DateField(label="Desde", required=False, widget=CampoFecha())
    hasta = forms.DateField(label="Hasta", required=False, widget=CampoFecha())
