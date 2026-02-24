# =========================
# board/urls.py
# Главные маршруты проекта
# =========================

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# Вьюхи верхнего уровня проекта
from board.views import home_view, signup_view, profile_view


urlpatterns = [
    # Главная
    path("", home_view, name="home"),

    # Админка
    path("admin/", admin.site.urls),

    # Авторизация
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup_view, name="signup"),

    # Профиль
    path("profile/", profile_view, name="profile"),

    # Объявления
    path("ads/", include("board.ads.urls")),
]

