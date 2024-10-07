from django.shortcuts import render
from django.http import HttpResponse


def landing_page(req):
    return HttpResponse("landin page")


def home(req):
    return HttpResponse("home")


def cart(req):
    return HttpResponse("cart")


def about(req):
    return HttpResponse("about")


def card_detail(req, prod_id):
    return HttpResponse(f"prod: {prod_id}")
