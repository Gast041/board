# =========================
# board/urls.py
# ГЛАВНЫЕ URL МАРШРУТЫ САЙТА
# =========================

# =========================
# ИМПОРТЫ DJANGO
# =========================
from django.contrib import admin                              # админка Django
from django.urls import path, include                         # path — маршрут, include — подключение urls другого приложения
from django.contrib.auth import views as auth_views           # готовые вьюхи Django для login/logout

# =========================
# ВЬЮХИ ОСНОВНОГО САЙТА
# =========================
# home_view — главная
# signup_view — регистрация
# profile_view — профиль
from board.views import home_view, signup_view, profile_view


# =========================
# СПИСОК URL МАРШРУТОВ ПРОЕКТА
# =========================
urlpatterns = [

    # -------------------------
    # ГЛАВНАЯ СТРАНИЦА
    # URL: /
    # -------------------------
    path("", home_view, name="home"),

    # -------------------------
    # ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
    # URL: /profile/
    # name="profile" нужен для {% url 'profile' %}
    # -------------------------
    path("profile/", profile_view, name="profile"),

    # -------------------------
    # АДМИНКА DJANGO
    # URL: /admin/
    # -------------------------
    path("admin/", admin.site.urls),

    # -------------------------
    # АВТОРИЗАЦИЯ
    # -------------------------

    # Вход
    # URL: /login/
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login"
    ),

    # Выход
    # URL: /logout/
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    # Регистрация
    # URL: /signup/
    path("signup/", signup_view, name="signup"),

    # -------------------------
    # ОБЪЯВЛЕНИЯ (ADS)
    # -------------------------
    # Всё, что начинается с /ads/ — уходит в board/ads/urls.py
    path("ads/", include("board.ads.urls")),
]


