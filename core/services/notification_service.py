from abc import ABC, abstractmethod
from django.core.mail import send_mail
from django.conf import settings
from core.models import NewsletterSubscriber


class Observer(ABC):
    """Patron Observer: Clase base abstracta"""
    
    @abstractmethod
    def update(self, product):
        pass


class EmailNotificationObserver(Observer):
    """Observador que envia notificaciones por email"""
    
    def update(self, product):
        subscribers = NewsletterSubscriber.objects.filter(is_active=True)
        
        if not subscribers.exists():
            print("No hay suscriptores activos")
            return
        
        subject = f'Nuevo producto: {product.name}'
        message = f'''
Hola!

Tenemos un nuevo producto para ti:

Nombre: {product.name}
Descripcion: {product.description}
Precio: ${product.price}
Categoria: {product.get_category_display()}

Visita nuestra tienda para mas detalles!

---
Senilit - Tu plataforma de productos
        '''
        
        recipient_list = [sub.email for sub in subscribers]
        
        try:
            # En desarrollo usa console backend
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            print(f"[OK] Newsletter enviado a {len(recipient_list)} suscriptores")
        except Exception as e:
            print(f"[ERROR] Error al enviar newsletter: {e}")


class ConsoleNotificationObserver(Observer):
    """Observador que imprime en consola"""
    
    def update(self, product):
        print(f"\n{'='*60}")
        print(f"NUEVO PRODUCTO CREADO")
        print(f"{'='*60}")
        print(f"Nombre: {product.name}")
        print(f"Precio: ${product.price}")
        print(f"Categoria: {product.get_category_display()}")
        print(f"Stock: {product.stock}")
        print(f"{'='*60}\n")


class NotificationService:
    """Servicio que gestiona observadores"""
    
    def __init__(self):
        self._observers = []
        self.attach(EmailNotificationObserver())
        self.attach(ConsoleNotificationObserver())
    
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify_new_product(self, product):
        """Notificar a todos los observadores"""
        for observer in self._observers:
            observer.update(product)
