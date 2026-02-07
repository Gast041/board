from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

# Главные вьюхи сайта (главная страница, регистрация)
from board.views import home_view, signup_view

# Вьюхи приложения объявлений
from board.ads.views import create_ad

urlpatterns = [

    # Главная страница сайта
    path("", home_view, name="home"),

    # Админка Django
    path("admin/", admin.site.urls),

    # Вход пользователя
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login"
    ),

    # Выход пользователя
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    # Регистрация пользователя
    path("signup/", signup_view, name="signup"),

    # Создание объявления (только для авторизованных)
    path("ads/create/", create_ad, name="create_ad"),
]
