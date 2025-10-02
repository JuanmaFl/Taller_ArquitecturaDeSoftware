from django.contrib.auth import authenticate, login

class AuthService:
    def authenticate_and_login(self, request, username, password):
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        return user