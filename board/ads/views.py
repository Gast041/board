# =========================
# board/ads/views.py
# ВЬЮХИ ПРИЛОЖЕНИЯ "ads"
# =========================

# =========================
# ИМПОРТЫ
# =========================

# render — отрисовать HTML-шаблон и вернуть страницу пользователю
# redirect — сделать перенаправление на другой URL
from django.shortcuts import render, redirect

# get_object_or_404 — достать объект из базы или вернуть 404
from django.shortcuts import get_object_or_404

# login_required — запрещает доступ неавторизованным пользователям
from django.contrib.auth.decorators import login_required

# HttpResponseForbidden — ответ 403 "Запрещено"
from django.http import HttpResponseForbidden

# Q — нужен для правильного объединения условий поиска (OR)
from django.db.models import Q

# Ad — модель объявления
from .models import Ad


# =========================
# ЛЕНТА ОБЪЯВЛЕНИЙ (СПИСОК) + ПОИСК
# =========================
def ads_list(request):
    """
    Лента объявлений + поиск.
    URL: /ads/?q=текст
    """

    # Берём текст из строки поиска
    q = request.GET.get("q", "").strip()

    # Базовый queryset (новые сверху)
    ads = Ad.objects.order_by("-id")

    # Если пользователь что-то ввёл — фильтруем
    if q:
        ads = ads.filter(
            Q(title__icontains=q) |       # поиск в заголовке
            Q(description__icontains=q)   # поиск в описании
        )

    return render(
        request,
        "ads/list.html",
        {
            "ads": ads,
            "q": q,   # возвращаем текст в поле поиска
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
    """

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()

        ad = Ad.objects.create(
            title=title,
            description=description,
            price=price if price else None,
            author=request.user
        )

        return redirect("ad_detail", ad_id=ad.id)

    return render(request, "ads/create_ad.html")


# =========================
# СТРАНИЦА ОДНОГО ОБЪЯВЛЕНИЯ
# =========================
def ad_detail(request, ad_id):
    """
    Детальная страница объявления.
    URL: /ads/<id>/
    """

    ad = get_object_or_404(Ad, id=ad_id)

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

    from .forms import AdForm

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
