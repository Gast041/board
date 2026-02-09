from django.urls import path
from . import views

urlpatterns = [
    path("", views.ads_list, name="ads_list"),          # /ads/
    path("create/", views.create_ad, name="create_ad"), # /ads/create/
]
path("ads/<int:ad_id>/", ad_detail, name="ad_detail"),