from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Ad

@login_required
def create_ad(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")

        Ad.objects.create(
            title=title,
            description=description,
            price=price,
            author=request.user
        )

        return redirect("/")  # потом заменишь на страницу объявления

    return render(request, "ads/create_ad.html")

def home_view(request):
    return render(request, "home.html")

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})

