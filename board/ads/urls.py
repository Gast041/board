# =========================
# URL МАРШРУТЫ ПРИЛОЖЕНИЯ ADS (объявления)
# Файл: board/ads/urls.py
# =========================

from django.urls import path              # path() — связывает URL и функцию-вьюху
from . import views                       # импортируем ВСЕ вьюхи из views.py этого приложения

urlpatterns = [
    # /ads/ → лента объявлений
    path("", views.ads_list, name="ads_list"),

    # /ads/create/ → создать объявление
    path("create/", views.create_ad, name="create_ad"),

    # /ads/123/ → страница одного объявления
    path("<int:ad_id>/", views.ad_detail, name="ad_detail"),
]
