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

# timezone — нужен для определения активных / архивных объявлений
from django.utils import timezone

# Кастомная форма регистрации
from .forms import SignupForm

# ВАЖНО: берём Category и Ad из приложения ads
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

    categories = (
        Category.objects
        .filter(is_active=True, parent__isnull=True)
        .prefetch_related("children")
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

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
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

    Показывает:
    - активные объявления
    - архивные / снятые с публикации
    """

    now = timezone.now()

    # -------------------------
    # АКТИВНЫЕ ОБЪЯВЛЕНИЯ
    # -------------------------
    active_ads = (
        Ad.objects
        .filter(author=request.user)
        .filter(status=Ad.STATUS_ACTIVE)
        .filter(expires_at__gt=now)
        .filter(deleted_by_user_at__isnull=True)
        .select_related("category", "category__parent")
        .order_by("-published_at", "-id")
    )

    # -------------------------
    # АРХИВНЫЕ / СНЯТЫЕ С ПУБЛИКАЦИИ
    # -------------------------
    archived_ads = (
        Ad.objects
        .filter(author=request.user)
        .exclude(
            status=Ad.STATUS_ACTIVE,
            expires_at__gt=now,
            deleted_by_user_at__isnull=True,
        )
        .select_related("category", "category__parent")
        .order_by("-published_at", "-id")
    )

    return render(
        request,
        "profile.html",
        {
            "active_ads": active_ads,
            "archived_ads": archived_ads,
        }
    )