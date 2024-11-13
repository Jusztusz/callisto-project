from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/ws/hardware')  # Ha már be van jelentkezve, irányítsuk a védett oldalra

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/ws/hardware')  # Sikeres bejelentkezés után irány a védett oldalra
    else:
        form = CustomLoginForm()

    return render(request, 'home.html', {'form': form})