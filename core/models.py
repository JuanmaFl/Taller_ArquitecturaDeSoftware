from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electrónica'),
        ('clothing', 'Ropa'),
        ('food', 'Alimentos'),
        ('books', 'Libros'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Categoría')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Creado por')
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Usuario')
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de suscripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        verbose_name = 'Suscriptor de Newsletter'
        verbose_name_plural = 'Suscriptores de Newsletter'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
