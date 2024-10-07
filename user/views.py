from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    UserCreationForm,  # crear formularios Create user
    AuthenticationForm,  # crear formularios login user
)
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError  # para menejar excepciones de la db
from django.contrib.auth.decorators import login_required


def signUp(request):
    print(request.method)

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
                login(
                    request, user
                )  # esto es bueenisimo para crear cookies y persistencia de datos "tiene expiracion"
                return redirect("home")
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
def signOut(request):
    logout(request)
    return redirect("landing")
