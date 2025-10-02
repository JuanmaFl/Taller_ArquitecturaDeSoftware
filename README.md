
---

##  Actividad 3 — Inversión de Dependencias:

### Objetivo:
Aplicar el principio de **Inversión de Dependencias** en una clase del proyecto para desacoplar la lógica de autenticación del controlador (vista), facilitando la reutilización, testeo y escalabilidad.

### Implementación:
Se creó la clase `AuthService` en `core/services/auth_service.py`, que encapsula la lógica de autenticación y login. La vista `register` ahora depende de esta abstracción en lugar de funciones concretas.

```python
# core/services/auth_service.py
from django.contrib.auth import authenticate, login

class AuthService:
    def authenticate_and_login(self, request, username, password):
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        return user
```

```python
# core/views.py
from .services.auth_service import AuthService

def register(request):
    ...
    if user_creation_form.is_valid():
        user_creation_form.save()
        auth_service = AuthService()
        user = auth_service.authenticate_and_login(
            request,
            user_creation_form.cleaned_data['username'],
            user_creation_form.cleaned_data['password1']
        )
        return redirect('home')
```

### Beneficios:
- Desacoplamiento entre vista y lógica de autenticación.
- Reusabilidad del servicio en otras vistas.
- Facilidad para pruebas unitarias.
- Mayor claridad y mantenibilidad del código.

---

## Actividad 4 — Aplicación de Patrón de Diseño (Strategy):

### Objetivo:
Aplicar el patrón de diseño **Strategy** para encapsular reglas de validación en el formulario de registro, permitiendo agregar nuevas validaciones sin modificar la clase base.

### Proceso de decisión:
Se eligió el patrón Strategy porque:
- El formulario `CustomUserCreationForm` requiere múltiples validaciones.
- Cada validación puede cambiar o crecer con el tiempo.
- Se busca mantener el formulario limpio y extensible.

### Implementación:

#### Interfaz base:
```python
# core/strategies/validation_strategy.py
from abc import ABC, abstractmethod

class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, form):
        pass
```

#### Estrategia concreta:
```python
# core/strategies/email_unique_strategy.py
from django.contrib.auth.models import User
from core.strategies.validation_strategy import ValidationStrategy

class EmailUniqueStrategy(ValidationStrategy):
    def validate(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Este correo electrónico ya está registrado')
```

#### Integración en el formulario:
```python
# core/forms.py
class CustomUserCreationForm(UserCreationForm):
    ...
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation_strategies = [EmailUniqueStrategy()]

    def is_valid(self):
        valid = super().is_valid()
        if valid:
            for strategy in self.validation_strategies:
                strategy.validate(self)
            if self.errors:
                return False
        return valid
```

### Beneficios:
- Validaciones desacopladas y reutilizables.
- Fácil extensión con nuevas estrategias.
- Código más limpio y mantenible.
- Mejora la testabilidad del formulario.

---

¿Quieres que te ayude a agregar una sección de instalación, ejecución o pruebas al README? También puedo ayudarte a redactar la introducción del proyecto si estás preparando la entrega final.
