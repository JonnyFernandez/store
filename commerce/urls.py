from django.urls import path
from .views import landing_page, home, cart, about, card_detail

urlpatterns = [
    path("", landing_page, name="landing"),
    path("home/", home, name="home"),
    path("cart/", cart, name="cart"),
    path("about/", about, name="about"),
    path("card_detail/<int:prod_id>", card_detail, name="card_detail"),
]
