from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    UserCreationForm,  # crear formularios Create user
    AuthenticationForm,  # crear formularios login user
)
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError  # para menejar excepciones de la db
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm


def signUp(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("add_info")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "El usuario ya existe"},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Password con coincide"},
        )


def signIn(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "usuario o contrasena incorrecto",
                },
            )
        else:
            login(request, user)
            return redirect("home")


@login_required
def add_info(request):

    # if request.user.is_authenticated:
    #     return redirect("home")

    print(request.method)
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Asocia el perfil con el usuario actual
            profile.save()
            return redirect("home")  # Redirige a la página que prefieras
    else:
        form = UserProfileForm()
    return render(request, "add_info.html", {"form": form})


@login_required
def signOut(request):
    logout(request)
    return redirect("home")
