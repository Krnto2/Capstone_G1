from django.core.exceptions import ValidationError


class RequisitosContrasena:
    """Al menos una mayúscula, un número y un carácter especial."""

    TEXTO = "Debe tener al menos una mayúscula, un número y un carácter especial."

    def validate(self, password, user=None):
        if not (any(c.isupper() for c in password) and any(c.isdigit() for c in password)
                and any(not c.isalnum() for c in password)):
            raise ValidationError(self.TEXTO, code="password_incompleta")

    def get_help_text(self):
        return self.TEXTO
