from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .templates.ads.views import home_view, signup_view
from .templates.ads import views

urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup_view, name="signup"),
    path("ads/create/", views.create_ad, name="create_ad"),
]
