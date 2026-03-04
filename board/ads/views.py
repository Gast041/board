# =========================
# Файл: board/ads/views.py
# ИСПРАВЛЕНИЕ: create_ad теперь работает через AdForm
# чтобы:
# - в шаблон приходил form
# - работала рубрика (category)
# - не было “ручного” request.POST
# =========================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q

from .models import Ad
from .forms import AdForm


def ads_list(request):
    q = request.GET.get("q", "").strip()
    ads = Ad.objects.order_by("-id")

    if q:
        ads = ads.filter(Q(title__icontains=q) | Q(description__icontains=q))

    return render(request, "ads/list.html", {"ads": ads, "q": q})


@login_required
def create_ad(request):
    """
    Создание объявления через AdForm.
    URL: /ads/create/
    """

    if request.method == "POST":
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect("ad_detail", ad_id=ad.id)
    else:
        form = AdForm()

    return render(request, "ads/create_ad.html", {"form": form})


def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, "ads/ad_detail.html", {"ad": ad})


@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.author != request.user:
        return HttpResponseForbidden("Нет прав: вы не автор этого объявления.")

    if request.method == "POST":
        ad.delete()
        return redirect("ads_list")

    return redirect("ad_detail", ad_id=ad.id)


@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.author != request.user:
        return HttpResponseForbidden("Нет прав: вы не автор этого объявления.")

    if request.method == "POST":
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect("ad_detail", ad_id=ad.id)
    else:
        form = AdForm(instance=ad)

    return render(request, "ads/edit_ad.html", {"form": form, "ad": ad})