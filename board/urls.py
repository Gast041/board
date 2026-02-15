# =========================
# ИМПОРТЫ DJANGO
# =========================
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from board.views import home_view, signup_view, profile_view  # + profile_view


# =========================
# ВЬЮХИ ОСНОВНОГО САЙТА
# (главная + регистрация)
# =========================
# Эти вьюхи относятся НЕ к объявлениям,
# а к самому сайту в целом
from board.views import home_view, signup_view


# Профиль пользователя
# /profile/
path("profile/", profile_view, name="profile"),



# =========================
# ГЛАВНЫЕ URL МАРШРУТЫ САЙТА
# =========================
urlpatterns = [

    # -------------------------
    # ГЛАВНАЯ СТРАНИЦА
    # /
    # -------------------------
    path("", home_view, name="home"),


    # -------------------------
    # АДМИНКА DJANGO
    # /admin/
    # -------------------------
    path("admin/", admin.site.urls),


    # -------------------------
    # АВТОРИЗАЦИЯ
    # -------------------------

    # Страница входа
    # /login/
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login"
    ),

    # Выход пользователя
    # /logout/
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    # Регистрация
    # /signup/
    path("signup/", signup_view, name="signup"),


    # -------------------------
    # ОБЪЯВЛЕНИЯ (ADS)
    # -------------------------
    # ВСЕ URL, начинающиеся с /ads/
    # Django будет искать в файле:
    # board/ads/urls.py
    #
    # Примеры:
    # /ads/          → список объявлений
    # /ads/create/   → создать объявление
    #
    path("ads/", include("board.ads.urls")),
]



