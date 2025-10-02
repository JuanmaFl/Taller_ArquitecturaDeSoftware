from django.contrib.auth.models import User
from core.strategies.validation_strategy import ValidationStrategy

class EmailUniqueStrategy(ValidationStrategy):
    def validate(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Este correo electrónico ya está registrado')