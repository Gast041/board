
# board/views.py
# =========================
# ВЬЮХИ "верхнего уровня"
# =========================


# =========================
# ИМПОРТЫ
# =========================


# render — рендерит HTML-шаблон
# redirect — делает перенаправление
from django.shortcuts import render, redirect

# login_required — запрещает доступ неавторизованным
from django.contrib.auth.decorators import login_required

# Кастомная форма регистрации
from .forms import SignupForm

# ВАЖНО: берём Category из приложения ads
from board.ads.models import Category, Ad

# =========================
# ГЛАВНАЯ СТРАНИЦА
# =========================
def home_view(request):
    """
    Главная страница сайта
    URL: /
    Шаблон: home.html

    ВАЖНО:
    - подтягиваем рубрики из БД
    - берём только 9 верхних рубрик (parent=None)
    - для каждой — до 5 подрубрик
    """

    # Верхние рубрики (родителя нет)
    categories = (
        Category.objects
        .filter(is_active=True, parent__isnull=True)
        .prefetch_related("children")  # подрубрики будут доступны как category.children.all()
        .order_by("sort_order", "name")[:9]
    )

    return render(
        request,
        "home.html",
        {"categories": categories}
    )



# =========================
# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
# =========================
def signup_view(request):
    """
    Страница регистрации
    URL: /signup/
    Шаблон: registration/signup.html
    """

    # Если форма отправлена
    if request.method == "POST":

        form = SignupForm(request.POST)

        # Проверяем корректность данных
        if form.is_valid():
            form.save()          # создаём пользователя
            return redirect("login")

    else:
        # Если просто открыли страницу
        form = SignupForm()

    return render(
        request,
        "registration/signup.html",
        {"form": form}
    )


# =========================
# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# =========================
@login_required
def profile_view(request):
    """
    Профиль пользователя
    URL: /profile/
    Показывает список его объявлений
    """

    # Берём только объявления текущего пользователя
    my_ads = Ad.objects.filter(
        author=request.user
    ).order_by("-id")

    return render(
        request,
        "profile.html",
        {
            "my_ads": my_ads
        }
    )

