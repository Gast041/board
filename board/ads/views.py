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

# Формы
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
    # Параметры из URL
    # -------------------------
    q = request.GET.get("q", "").strip()
    cat = request.GET.get("cat", "").strip()

    # -------------------------
    # Базовый queryset
    # -------------------------
    # select_related:
    # - author
    # - category
    # - category__parent
    # чтобы не делать лишние запросы в шаблоне
    # -------------------------
    ads = (
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

        # Если подрубрика найдена — фильтруем по ней
        if selected_category:
            ads = ads.filter(category=selected_category)
        else:
            # Если slug битый/не найден — показываем пустой результат
            ads = ads.none()

    # -------------------------
    # Поиск по заголовку/описанию
    # -------------------------
    if q:
        ads = ads.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    # -------------------------
    # Рендер
    # -------------------------
    return render(
        request,
        "ads/list.html",
        {
            "ads": ads,
            "q": q,
            "cat": cat,
            "selected_category": selected_category,
        }
    )


# =========================
# СОЗДАНИЕ ОБЪЯВЛЕНИЯ
# =========================
@login_required
def create_ad(request):
    """
    Создание объявления.
    URL: /ads/create/

    БЕЗ JS:
    - рубрика выбирается первой
    - после выбора рубрики страница перерисовывается
    - подрубрики подгружаются через GET-параметр parent_category
    """

    selected_parent_id = request.GET.get("parent_category")

    if request.method == "POST":
        form = AdForm(request.POST)

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
    """
    Детальная страница объявления.
    URL: /ads/<id>/
    """
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
    """
    Удаление объявления.
    URL: /ads/<id>/delete/
    """
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
    """
    Редактирование объявления.
    URL: /ads/<id>/edit/

    Логика:
    - сначала рубрика
    - потом подрубрика
    """

    ad = get_object_or_404(Ad, id=ad_id)

    if ad.author != request.user:
        return HttpResponseForbidden("Нет прав: вы не автор этого объявления.")

    selected_parent_id = request.GET.get("parent_category")

    if request.method == "POST":
        form = AdForm(request.POST, instance=ad)

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