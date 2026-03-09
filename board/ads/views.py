# =========================
# board/ads/views.py
# ВЬЮХИ ПРИЛОЖЕНИЯ "ads"
# =========================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Ad, Category
from .forms import AdForm


# =========================
# ЛЕНТА ОБЪЯВЛЕНИЙ (СПИСОК) + ПОИСК + ФИЛЬТР ПО РУБРИКЕ + ПАГИНАЦИЯ
# =========================
def ads_list(request):
    """
    Лента объявлений.

    Поддерживает:
    - поиск: /ads/?q=текст
    - фильтр по подрубрике: /ads/?cat=slug
    - пагинацию: /ads/?page=2
    """

    # -------------------------
    # Параметры из URL
    # -------------------------
    q = request.GET.get("q", "").strip()
    cat = request.GET.get("cat", "").strip()
    page_number = request.GET.get("page")

    # -------------------------
    # Базовый queryset
    # -------------------------
    ads_queryset = (
        Ad.objects
        .select_related("author", "category", "category__parent")
        .order_by("-id")
    )

    # -------------------------
    # Выбранная подрубрика
    # -------------------------
    selected_category = None

    if cat:
        selected_category = (
            Category.objects
            .select_related("parent")
            .filter(slug=cat, is_active=True)
            .first()
        )

        if selected_category:
            ads_queryset = ads_queryset.filter(category=selected_category)
        else:
            ads_queryset = ads_queryset.none()

    # -------------------------
    # Поиск
    # -------------------------
    if q:
        ads_queryset = ads_queryset.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    # -------------------------
    # ПАГИНАЦИЯ
    # 10 объявлений на страницу
    # -------------------------
    paginator = Paginator(ads_queryset, 10)
    ads = paginator.get_page(page_number)

    return render(
        request,
        "ads/list.html",
        {
            "ads": ads,
            "q": q,
            "cat": cat,
            "selected_category": selected_category,
            "page_obj": ads,
            "is_paginated": ads.has_other_pages(),
        }
    )


# =========================
# СОЗДАНИЕ ОБЪЯВЛЕНИЯ
# =========================
@login_required
def create_ad(request):
    selected_parent_id = request.GET.get("parent_category")

    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)

        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect("ad_detail", ad_id=ad.id)
    else:
        form = AdForm(parent_id=selected_parent_id)

    return render(
        request,
        "ads/create_ad.html",
        {
            "form": form,
            "selected_parent_id": selected_parent_id,
        }
    )


# =========================
# СТРАНИЦА ОДНОГО ОБЪЯВЛЕНИЯ
# =========================
def ad_detail(request, ad_id):
    ad = get_object_or_404(
        Ad.objects.select_related("author", "category", "category__parent"),
        id=ad_id
    )

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
    ad = get_object_or_404(Ad, id=ad_id)

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
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.author != request.user:
        return HttpResponseForbidden("Нет прав: вы не автор этого объявления.")

    selected_parent_id = request.GET.get("parent_category")

    if request.method == "POST":
        form = AdForm(request.POST, request.FILES, instance=ad)

        if form.is_valid():
            form.save()
            return redirect("ad_detail", ad_id=ad.id)
    else:
        form = AdForm(instance=ad, parent_id=selected_parent_id)

    return render(
        request,
        "ads/edit_ad.html",
        {
            "form": form,
            "ad": ad,
            "selected_parent_id": selected_parent_id,
        }
    )