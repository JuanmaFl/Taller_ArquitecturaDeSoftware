from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.strategies.email_unique_strategy import EmailUniqueStrategy
from core.models import Product, NewsletterSubscriber

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
            if self.errors:
                return False
        return valid

class ProductForm(forms.ModelForm):
    """Formulario para crear productos usando Factory Pattern"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Laptop Dell XPS 15'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción detallada del producto...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0', 'min': '0'}),
        }

class NewsletterSubscriptionForm(forms.ModelForm):
    """Formulario para suscribirse al newsletter"""
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'}),
        }
