## Actividad 1 - Repositorio
**Repositorio GitHub:** https://github.com/JuanmaFl/Taller_ArquitecturaDeSoftware

***

## Actividad 2 - Revisión Autocrítica

**Aspectos positivos:**
- Autenticación funcional con Django
- Interfaz responsive con Bootstrap
- Protección CSRF en formularios

**Aspectos a mejorar:**
- Lógica de autenticación mezclada en vistas (aplicamos inversión de dependencias)
- Validaciones no reutilizables (aplicamos Strategy Pattern)
- Sin sistema de notificaciones (implementamos Observer Pattern)
- Mejora general y limpieza del codigo
---

## Actividad 3 - Inversión de Dependencias

Separamos la lógica de autenticación de las vistas.

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
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            auth_service = AuthService()
            auth_service.authenticate_and_login(
                request,
                form.cleaned_data['username'],
                form.cleaned_data['password1']
            )
            return redirect('home')
```

**Beneficio:** Vista desacoplada, código reutilizable y testeable.

***

## Actividad 4 - Patrón Strategy (Python)

Validaciones reutilizables con Strategy Pattern.

```python
# core/strategies/validation_strategy.py
from abc import ABC, abstractmethod

class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, form):
        pass
```

```python
# core/strategies/email_unique_strategy.py
from django.contrib.auth.models import User
from core.strategies.validation_strategy import ValidationStrategy

class EmailUniqueStrategy(ValidationStrategy):
    def validate(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Este correo ya está registrado')
```

```python
# core/forms.py
class CustomUserCreationForm(UserCreationForm):
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

**Beneficio:** Fácil agregar validaciones sin modificar código existente.

***

## Actividad 5 - Patrones Django

### Factory Pattern
Crea productos según categoría automáticamente.

```python
# core/factories/product_factory.py
class ProductFactoryProvider:
    _factories = {
        'electronics': ElectronicsProductFactory,
        'clothing': ClothingProductFactory,
    }
    
    @classmethod
    def get_factory(cls, category):
        return cls._factories[category]()
```

### Observer Pattern
Notifica a suscriptores cuando se crea un producto.

```python
# core/services/notification_service.py
class NotificationService:
    def __init__(self):
        self._observers = [EmailNotificationObserver(), ConsoleNotificationObserver()]
    
    def notify_new_product(self, product):
        for observer in self._observers:
            observer.update(product)
```

**Beneficio:** Desacoplamiento entre creación y notificaciones.

***

## BONO - Newsletter

Sistema de notificaciones que avisa cuando se agregan productos.

**Modelo:**
```python
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
```

**Vista:**
```python
def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            NewsletterSubscriber.objects.create(email=form.cleaned_data['email'])
```

Usa Factory + Observer para notificar automáticamente.

---
