from django.core.exceptions import ValidationError


class AlfanumericoValidator:
    """RNF-02: la contraseña debe combinar letras y números."""

    def validate(self, password, user=None):
        if not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
            raise ValidationError("La contraseña debe contener letras y números.", code="password_no_alfanumerica")

    def get_help_text(self):
        return "La contraseña debe contener letras y números."
