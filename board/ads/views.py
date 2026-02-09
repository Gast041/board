# =========================
# ИМПОРТЫ
# =========================

# render — отрисовывает HTML-шаблон
# redirect — делает перенаправление на другой URL
from django.shortcuts import render, redirect

# Декоратор: запрещает доступ неавторизованным пользователям
from django.contrib.auth.decorators import login_required

# Встроенная форма Django для регистрации пользователей
from django.contrib.auth.forms import UserCreationForm

# Модель объявления Ad
# ВАЖНО: импорт из ТЕКУЩЕГО приложения ads
from .models import Ad


# =========================
# СОЗДАНИЕ ОБЪЯВЛЕНИЯ
# =========================
def ads_list(request):
    ads = Ad.objects.order_by("-id")  # новые сверху
    return render(request, "ads/list.html", {"ads": ads})

@login_required
def create_ad(request):
    """
    Страница 'Разместить объявление'
    Пользователь ОБЯЗАН быть авторизован
    """

    # Если форма отправлена (нажата кнопка)
    if request.method == "POST":

        # Получаем данные из HTML-формы
        title = request.POST.get("title")          # заголовок
        description = request.POST.get("description")  # описание
        price = request.POST.get("price")          # цена

        # Создаём новое объявление в базе данных
        Ad.objects.create(
            title=title,
            description=description,
            price=price,
            author=request.user    # автор — текущий пользователь
        )

        # После создания объявления возвращаем на главную
        return redirect("/")

    # Если просто открыли страницу — показываем форму
    return render(request, "ads/create_ad.html")


# =========================
# ГЛАВНАЯ СТРАНИЦА
# =========================

def home_view(request):
    """
    Главная страница сайта
    """
    return render(request, "home.html")


# =========================
# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
# =========================

def signup_view(request):
    """
    Регистрация нового пользователя
    """

    # Если пользователь отправил форму
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        # Проверяем корректность данных
        if form.is_valid():
            form.save()              # создаём пользователя
            return redirect("login") # отправляем на страницу входа

    # Если просто открыли страницу регистрации
    else:
        form = UserCreationForm()

    # Отрисовываем шаблон регистрации
    return render(
        request,
        "registration/signup.html",
        {"form": form}
    )
def ad_detail(request, ad_id):
    return render(request, "ads/ad_detail.html", {
        "ad_id": ad_id
    })
