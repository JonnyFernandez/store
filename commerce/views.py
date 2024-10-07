from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def landing_page(req):
    prod = Product.objects.all()
    return render(req, "home.html", {"prod": prod})


def home(req):
    return HttpResponse("home")


def cart(req):
    return HttpResponse("cart")


def about(req):
    return HttpResponse("about")


def card_detail(req, prod_id):
    return HttpResponse(f"prod: {prod_id}")
