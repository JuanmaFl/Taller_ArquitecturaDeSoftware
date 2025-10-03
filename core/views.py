from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProductForm, NewsletterSubscriptionForm
from .services.auth_service import AuthService
from .factories.product_factory import ProductFactoryProvider
from .models import Product, NewsletterSubscriber

def home(request):
    return render(request, 'core/home.html')

@login_required
def products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'core/products.html', {'products': products})

@login_required
def create_product(request):
    """Vista para crear productos usando Factory Pattern"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                # Obtener la factory correcta según la categoría
                category = form.cleaned_data['category']
                factory = ProductFactoryProvider.get_factory(category)
                
                # Crear el producto usando la factory
                product = factory.create_product(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                    price=form.cleaned_data['price'],
                    stock=form.cleaned_data['stock'],
                    created_by=request.user
                )
                
                subscriber_count = NewsletterSubscriber.objects.filter(is_active=True).count()
                messages.success(
                    request, 
                    f'✓ Producto "{product.name}" creado exitosamente. '
                    f'Se notificó a {subscriber_count} suscriptor(es).'
                )
                return redirect('products')
            except Exception as e:
                messages.error(request, f'Error al crear el producto: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ProductForm()
    
    return render(request, 'core/create_product.html', {'form': form})

def subscribe_newsletter(request):
    """Vista para suscribirse al newsletter"""
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'user': request.user if request.user.is_authenticated else None}
            )
            
            if created:
                messages.success(request, '✓ ¡Te has suscrito exitosamente al newsletter!')
            else:
                if subscriber.is_active:
                    messages.info(request, 'Ya estás suscrito al newsletter.')
                else:
                    subscriber.is_active = True
                    subscriber.save()
                    messages.success(request, '✓ ¡Tu suscripción ha sido reactivada!')
            
            return redirect('home')
    else:
        form = NewsletterSubscriptionForm()
    
    return render(request, 'core/subscribe_newsletter.html', {'form': form})

def register(request):
    data = {'form': CustomUserCreationForm()}
    
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            auth_service = AuthService()
            auth_service.authenticate_and_login(
                request,
                user_creation_form.cleaned_data['username'],
                user_creation_form.cleaned_data['password1']
            )
            return redirect('home')
        else:
            data['form'] = user_creation_form
    
    return render(request, 'registration/register.html', data)
