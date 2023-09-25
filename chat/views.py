from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

from .forms import CustomUserCreationForm


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("ttt:index")
        return render(request, "registration/register.html", {"form": form})
    elif request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("ttt:index")
        else:
            form = AuthenticationForm(request.POST)
            return render(
                request,
                "registration/login.html",
                {
                    "form": form,
                    "error": "Please enter a correct username and password.",
                },
            )
    elif request.method == "GET":
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("ttt:login")
