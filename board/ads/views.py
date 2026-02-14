# =========================
# board/ads/views.py
# ВЬЮХИ ПРИЛОЖЕНИЯ "ads"
# =========================

# =========================
# ИМПОРТЫ
# =========================

# render — отрисовать HTML-шаблон и вернуть страницу пользователю
# redirect — сделать перенаправление на другой URL (например после сохранения формы)
from django.shortcuts import render, redirect

# get_object_or_404 — достать объект из базы или вернуть 404, если не найден
from django.shortcuts import get_object_or_404

# login_required — запрещает доступ неавторизованным пользователям
# (если не залогинен — отправит на LOGIN_URL из settings.py)
from django.contrib.auth.decorators import login_required

# HttpResponseForbidden — ответ 403 "Запрещено" (если не автор объявления)
from django.http import HttpResponseForbidden

# Ad — модель объявления из текущего приложения "ads"
from .models import Ad


# =========================
# ЛЕНТА ОБЪЯВЛЕНИЙ (СПИСОК)
# =========================
def ads_list(request):
    """
    Лента объявлений.
    URL: /ads/
    Шаблон: templates/ads/list.html
    """

    # Берём все объявления из базы данных
    # order_by("-id") — сортировка: новые сверху (по убыванию id)
    ads = Ad.objects.order_by("-id")

    # Рендерим шаблон и передаём в него список объявлений
    return render(
        request,                  # текущий запрос
        "ads/list.html",          # путь к шаблону
        {"ads": ads}              # данные, доступные в шаблоне
    )


# =========================
# СОЗДАНИЕ ОБЪЯВЛЕНИЯ
# =========================
@login_required
def create_ad(request):
    """
    Создание объявления.
    URL: /ads/create/
    Шаблон: templates/ads/create_ad.html
    Доступ: только авторизованным
    """

    # Если пользователь отправил форму (POST)
    if request.method == "POST":

        # Берём значения из формы (input name="title" и т.д.)
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()

        # Создаём запись в базе данных
        ad = Ad.objects.create(
            title=title,                           # заголовок
            description=description,               # описание
            price=price if price else None,        # если пусто — записываем NULL
            author=request.user                    # автор — текущий пользователь
        )

        # После создания отправляем на страницу созданного объявления
        return redirect("ad_detail", ad_id=ad.id)

    # Если запрос GET — просто показываем страницу формы
    return render(request, "ads/create_ad.html")


# =========================
# СТРАНИЦА ОДНОГО ОБЪЯВЛЕНИЯ
# =========================
def ad_detail(request, ad_id):
    """
    Детальная страница объявления.
    URL: /ads/<id>/
    Шаблон: templates/ads/ad_detail.html
    """

    # Ищем объявление по id
    # Если не найдено — Django автоматически покажет страницу 404
    ad = get_object_or_404(Ad, id=ad_id)

    # Передаём найденное объявление в шаблон
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
    Доступ: только авторизованным и только автору объявления

    Логика:
    1) Находим объявление
    2) Проверяем, что текущий пользователь — автор
    3) Удаляем ТОЛЬКО по POST (это важно для безопасности)
    4) После удаления кидаем в ленту /ads/
    """

    # 1) Достаём объявление или 404
    ad = get_object_or_404(Ad, id=ad_id)

    # 2) Проверяем автора
    if ad.author != request.user:
        # 403 — запрещено
        return HttpResponseForbidden("Нет прав: вы не автор этого объявления.")

    # 3) Удаляем только если нажали кнопку (POST)
    if request.method == "POST":
        ad.delete()
        # 4) После удаления — в ленту
        return redirect("ads_list")

    # Если кто-то открыл URL удаления через GET — просто кидаем на страницу объявления
    return redirect("ad_detail", ad_id=ad.id)
# =========================
# РЕДАКТИРОВАНИЕ ОБЪЯВЛЕНИЯ (ТОЛЬКО АВТОР)
# =========================
@login_required
def edit_ad(request, ad_id):
    """
    Редактирование объявления.
    URL: /ads/<id>/edit/
    Доступ: только авторизованным и только автору объявления
    """

    # 1) Достаём объявление или 404
    ad = get_object_or_404(Ad, id=ad_id)

    # 2) Проверяем, что текущий пользователь — автор
    if ad.author != request.user:
        return HttpResponseForbidden("Нет прав: вы не автор этого объявления.")

    # 3) Если отправили форму — сохраняем
    if request.method == "POST":
        # ВАЖНО: используем Django Form, а не request.POST руками
        from .forms import AdForm
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect("ad_detail", ad_id=ad.id)
    else:
        # 4) Если просто открыли страницу — показываем форму с текущими данными
        from .forms import AdForm
        form = AdForm(instance=ad)

    return render(request, "ads/edit_ad.html", {"form": form, "ad": ad})
