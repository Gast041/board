# board/views.py
# Вьюхи "верхнего уровня" проекта (не связанные с объявлениями)

# =========================
# ИМПОРТЫ
# =========================

# render — рендерит HTML-шаблон
# redirect — делает перенаправление на другой URL
from django.shortcuts import render, redirect

# Кастомная форма регистрации (ты её создал сам)
from .forms import SignupForm


# =========================
# ГЛАВНАЯ СТРАНИЦА
# =========================
def home_view(request):
    """
    Главная страница сайта
    URL: /
    Шаблон: home.html
    """

    # Просто показываем шаблон главной страницы
    return render(request, "home.html")


# =========================
# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
# =========================
def signup_view(request):
    """
    Страница регистрации пользователя
    URL: /signup/
    Шаблон: registration/signup.html
    """

    # Если пользователь отправил форму (нажал кнопку)
    if request.method == "POST":

        # Создаём форму и заполняем её данными из POST-запроса
        form = SignupForm(request.POST)

        # Проверяем, что все поля заполнены корректно
        if form.is_valid():

            # Сохраняем пользователя в базе данных
            form.save()

            # После успешной регистрации отправляем на страницу входа
            return redirect("login")

    else:
        # Если просто зашли на страницу — создаём пустую форму
        form = SignupForm()

    # Показываем страницу регистрации и передаём форму в шаблон
    return render(
        request,
        "registration/signup.html",
        {"form": form}
    )
# =========================
# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# =========================

from django.contrib.auth.decorators import login_required  # доступ только после входа
from board.ads.models import Ad  # объявления (чтобы показать "мои объявления")


@login_required
def profile_view(request):
    """
    Профиль пользователя.
    URL: /profile/
    Показывает имя пользователя и его объявления.
    """

    # Берём объявления, созданные текущим пользователем (новые сверху)
    my_ads = Ad.objects.filter(author=request.user).order_by("-id")

    # Отдаём HTML-шаблон и данные в него
    return render(
        request,                  # текущий запрос
        "profile.html",           # шаблон
        {"my_ads": my_ads}        # данные для шаблона
    )
