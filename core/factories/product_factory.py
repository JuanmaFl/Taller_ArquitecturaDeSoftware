from abc import ABC, abstractmethod
from core.models import Product
from core.services.notification_service import NotificationService

class ProductFactory(ABC):
    """
    Patrón Factory: Clase base abstracta para crear productos
    """
    
    @abstractmethod
    def create_product(self, **kwargs):
        pass
    
    def notify_subscribers(self, product):
        """Notifica a los suscriptores después de crear el producto"""
        notification_service = NotificationService()
        notification_service.notify_new_product(product)

class ElectronicsProductFactory(ProductFactory):
    def create_product(self, **kwargs):
        kwargs['category'] = 'electronics'
        product = Product.objects.create(**kwargs)
        self.notify_subscribers(product)
        return product

class ClothingProductFactory(ProductFactory):
    def create_product(self, **kwargs):
        kwargs['category'] = 'clothing'
        product = Product.objects.create(**kwargs)
        self.notify_subscribers(product)
        return product

class FoodProductFactory(ProductFactory):
    def create_product(self, **kwargs):
        kwargs['category'] = 'food'
        product = Product.objects.create(**kwargs)
        self.notify_subscribers(product)
        return product

class BooksProductFactory(ProductFactory):
    def create_product(self, **kwargs):
        kwargs['category'] = 'books'
        product = Product.objects.create(**kwargs)
        self.notify_subscribers(product)
        return product

class ProductFactoryProvider:
    """Proveedor central que devuelve la factory correcta"""
    
    _factories = {
        'electronics': ElectronicsProductFactory,
        'clothing': ClothingProductFactory,
        'food': FoodProductFactory,
        'books': BooksProductFactory,
    }
    
    @classmethod
    def get_factory(cls, category):
        factory_class = cls._factories.get(category)
        if not factory_class:
            raise ValueError(f"Categoría {category} no soportada")
        return factory_class()
