# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views import View  # Importamos a classe View
from django.contrib.auth.mixins import LoginRequiredMixin # Importamos o mixin

# A view de login e logout continua a mesma por enquanto.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Login bem-sucedido. Bem-vindo(a), {user.email}!")
                return redirect('home')
            else:
                messages.error(request, "E-mail ou senha inválidos.")
        else:
            messages.error(request, "E-mail ou senha inválidos.")
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta com sucesso.")
    return redirect('login')

# A view da página inicial agora será uma Class-Based View
class HomeView(LoginRequiredMixin, View):
    """
    Esta view da página inicial agora exige login.
    O LoginRequiredMixin garante que, se o usuário não estiver autenticado,
    ele seja redirecionado para a página de login.
    """
    def get(self, request):
        return render(request, 'core/home.html')