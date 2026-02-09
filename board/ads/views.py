# =========================
# ИМПОРТЫ
# =========================

# render — отрисовка HTML-шаблонов
# redirect — перенаправление на другой URL
from django.shortcuts import render, redirect

# login_required — запрещает доступ неавторизованным пользователям
from django.contrib.auth.decorators import login_required

# Модель объявления (ОБЯЗАТЕЛЬНО из текущего приложения ads)
from .models import Ad


# =========================
# ЛЕНТА ОБЪЯВЛЕНИЙ
# =========================
def ads_list(request):
    """
    Страница со списком объявлений (лента)
    URL: /ads/
    """

    # Получаем все объявления из базы данных
    # order_by("-id") — новые объявления сверху
    ads = Ad.objects.order_by("-id")

    # Передаём список объявлений в шаблон
    return render(
        request,
        "ads/list.html",
        {
            "ads": ads
        }
    )


# =========================
# СОЗДАНИЕ ОБЪЯВЛЕНИЯ
# =========================
@login_required
def create_ad(request):
    """
    Страница 'Разместить объявление'
    Пользователь ОБЯЗАН быть авторизован
    URL: /ads/create/
    """

    # Если форма отправлена (POST-запрос)
    if request.method == "POST":

        # Забираем данные из HTML-формы
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")

        # Создаём новое объявление в базе данных
        Ad.objects.create(
            title=title,
            description=description,
            price=price,
            author=request.user  # автор — текущий пользователь
        )

        # После создания объявления
        # перенаправляем пользователя в ленту
        return redirect("/ads/")

    # Если просто открыли страницу — показываем форму
    return render(request, "ads/create_ad.html")


# =========================
# СТРАНИЦА ОДНОГО ОБЪЯВЛЕНИЯ
# =========================
def ad_detail(request, ad_id):
    """
    Детальная страница одного объявления
    URL: /ads/<id>/
    """

    # Пока БЕЗ базы — просто передаём id в шаблон
    # Это безопасная заглушка
    return render(
        request,
        "ads/ad_detail.html",
        {
            "ad_id": ad_id
        }
    )
