from django.shortcuts import render
from django.http import HttpResponse


def signIn(req):
    return render(req, "signin.html", {})


def signUp(req):
    return render(req, "signup.html", {})


def signOut(req):
    return render(req, "signup.html", {})
