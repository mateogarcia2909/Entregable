from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from .forms import EditarPerfilForm 
from .models import Perfil


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

def registro_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('usuarios:registro')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        messages.success(request, 'Usuario registrado correctamente.')
        return redirect('usuarios:login')
    
    return render(request, 'usuarios/registro.html')

def login_usuario(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('usuarios:login')


@login_required
def perfil_usuario(request):
    perfil = request.user.perfil  # gracias al OneToOneField
    return render(request, 'usuarios/perfil.html', {'perfil': perfil})

@login_required(login_url='usuarios:login')
def editar_perfil(request):
    perfil = request.user.perfil

    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=perfil, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('usuarios:perfil')
    else:
        form = EditarPerfilForm(instance=perfil, user=request.user)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})
