from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignupForm

def login_page(request):
    return redirect('home')

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

def home_page(request):
    if request.user.is_authenticated:
        return redirect('flux')

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
                next_url = request.POST.get('next') or request.GET.get('next')
                return redirect(next_url or 'flux')
            message = 'Identifiants invalides.'

    return render(request, 'authentication/home.html', {'form': form, 'message': message})