# board/views.py

from django.shortcuts import render, redirect
from .forms import SignupForm

def home_view(request):
    # Показывает главную страницу (home.html)
    return render(request, "home.html")

def signup_view(request):
    # Если нажали кнопку "Зарегистрироваться"
    if request.method == "POST":
        form = SignupForm(request.POST)   # Берём данные из формы
        if form.is_valid():               # Проверяем валидность
            form.save()                   # Создаём пользователя
            return redirect("login")      # После регистрации — на страницу входа
    else:
        form = SignupForm()               # Пустая форма при открытии страницы

    # Рендерим шаблон регистрации и передаём туда форму
    return render(request, "registration/signup.html", {"form": form})
