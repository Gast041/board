# board/views.py
# =========================
# ВЬЮХИ "верхнего уровня"
# =========================


# =========================
# ИМПОРТЫ
# =========================

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone

from .forms import SignupForm
from board.ads.models import Category, Ad


# =========================
# ГЛАВНАЯ СТРАНИЦА
# =========================
def home_view(request):
    """
    Главная страница сайта
    URL: /
    Шаблон: home.html
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
    - на модерации
    - отклонённые
    - архив
    """

    now = timezone.now()

    base_qs = (
        Ad.objects
        .filter(author=request.user)
        .select_related("category", "category__parent", "reviewed_by")
        .order_by("-created_at", "-id")
    )

    active_ads = base_qs.filter(
        status=Ad.STATUS_ACTIVE,
        expires_at__gt=now,
        deleted_by_user_at__isnull=True,
    )

    pending_ads = base_qs.filter(
        status=Ad.STATUS_PENDING,
        deleted_by_user_at__isnull=True,
    )

    rejected_ads = base_qs.filter(
        status=Ad.STATUS_REJECTED,
        deleted_by_user_at__isnull=True,
    )

    archived_ads = base_qs.filter(
        Q(status=Ad.STATUS_ARCHIVED) |
        Q(expires_at__lte=now) |
        Q(deleted_by_user_at__isnull=False)
    ).exclude(status=Ad.STATUS_PENDING).exclude(status=Ad.STATUS_REJECTED)

    return render(
        request,
        "profile.html",
        {
            "active_ads": active_ads,
            "pending_ads": pending_ads,
            "rejected_ads": rejected_ads,
            "archived_ads": archived_ads,
        }
    )
