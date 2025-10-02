from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from .services.auth_service import AuthService  # Nuevo servicio importado

def home(request):
    return render(request, 'core/home.html')

@login_required
def products(request):
    return render(request, 'core/products.html')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            auth_service = AuthService()
            user = auth_service.authenticate_and_login(
                request,
                user_creation_form.cleaned_data['username'],
                user_creation_form.cleaned_data['password1']
            )

            return redirect('home')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)
