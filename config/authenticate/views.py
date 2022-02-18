from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import UserRegisterForm


def register(request):
    """Регистрация пользователя на сайте"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')

    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})
