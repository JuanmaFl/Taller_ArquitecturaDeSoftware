from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.strategies.email_unique_strategy import EmailUniqueStrategy

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation_strategies = [EmailUniqueStrategy()]

    def is_valid(self):
        valid = super().is_valid()
        if valid:
            for strategy in self.validation_strategies:
                strategy.validate(self)
            # Si las estrategias agregaron errores, el formulario no es válido
            if self.errors:
                return False
        return valid