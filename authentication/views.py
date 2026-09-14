from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout


def login_page(request):
    form = AuthenticationForm()
    message = ''

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('flux')
            message = 'Identifiants invalides.'

    return render(request, 'authentication/login.html', {'form': form, 'message': message})


def signup_page(request):
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('flux')

    return render(request, 'authentication/signup.html', {'form': form})

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('flux')