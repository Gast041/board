# =========================
# board/ads/views.py
# ВЬЮХИ ПРИЛОЖЕНИЯ "ads"
# =========================

# =========================
# ИМПОРТЫ
# =========================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q

# Модели
from .models import Ad, Category

# Форма объявлений (теперь и create, и edit через неё)
from .forms import AdForm


# =========================
# ЛЕНТА ОБЪЯВЛЕНИЙ (СПИСОК) + ПОИСК + ФИЛЬТР ПО РУБРИКЕ
# =========================
def ads_list(request):
    """
    Лента объявлений + поиск + фильтр по рубрике.
    URL:
      /ads/
      /ads/?q=текст
      /ads/?cat=slug_подрубрики
    """

    # -------------------------
    # 1) Параметры из URL
    # -------------------------
    q = request.GET.get("q", "").strip()
    cat = request.GET.get("cat", "").strip()   # slug подрубрики

    # -------------------------
    # 2) Базовый queryset
    # -------------------------
    ads = Ad.objects.select_related("author", "category").order_by("-id")

    # -------------------------
    # 3) Фильтр по категории (если передали ?cat=...)
    # -------------------------
    if cat:
        ads = ads.filter(category__slug=cat)

    # -------------------------
    # 4) Поиск (если ввели текст)
    # -------------------------
    if q:
        ads = ads.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    # -------------------------
    # 5) Рендер
    # -------------------------
    return render(
        request,
        "ads/list.html",
        {
            "ads": ads,
            "q": q,
            "cat": cat,   # пригодится подсветить выбранную рубрику/сброс
        }
    )


# =========================
# СОЗДАНИЕ ОБЪЯВЛЕНИЯ (через AdForm)
# =========================
@login_required
def create_ad(request):
    """
    Создание объявления.
    URL: /ads/create/

    ВАЖНО:
    - теперь сохраняем рубрику (category)
    - используем одну и ту же форму, что и в edit_ad
    """

    if request.method == "POST":
        form = AdForm(request.POST)

        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect("ad_detail", ad_id=ad.id)
    else:
        form = AdForm()

    return render(
        request,
        "ads/create_ad.html",
        {"form": form}
    )


# =========================
# СТРАНИЦА ОДНОГО ОБЪЯВЛЕНИЯ
# =========================
def ad_detail(request, ad_id):
    """
    Детальная страница объявления.
    URL: /ads/<id>/
    """
    ad = get_object_or_404(Ad.objects.select_related("author", "category"), id=ad_id)

    return render(
        request,
        "ads/ad_detail.html",
        {"ad": ad}
    )


# =========================
# УДАЛЕНИЕ ОБЪЯВЛЕНИЯ (ТОЛЬКО АВТОР)
# =========================
@login_required
def delete_ad(request, ad_id):
    """
    Удаление объявления.
    URL: /ads/<id>/delete/
    """
    ad = get_object_or_404(Ad, id=ad_id)

    # Проверка прав
    if ad.author != request.user:
        return HttpResponseForbidden("Нет прав: вы не автор этого объявления.")

    if request.method == "POST":
        ad.delete()
        return redirect("ads_list")

    return redirect("ad_detail", ad_id=ad.id)


# =========================
# РЕДАКТИРОВАНИЕ ОБЪЯВЛЕНИЯ (ТОЛЬКО АВТОР)
# =========================
@login_required
def edit_ad(request, ad_id):
    """
    Редактирование объявления.
    URL: /ads/<id>/edit/
    """
    ad = get_object_or_404(Ad, id=ad_id)

    # Проверка прав
    if ad.author != request.user:
        return HttpResponseForbidden("Нет прав: вы не автор этого объявления.")

    if request.method == "POST":
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect("ad_detail", ad_id=ad.id)
    else:
        form = AdForm(instance=ad)

    return render(
        request,
        "ads/edit_ad.html",
        {"form": form, "ad": ad}
    )