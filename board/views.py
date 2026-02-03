from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login

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

