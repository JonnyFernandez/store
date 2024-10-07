from django.urls import path
from .views import (
    landing_page,
    home,
    view_cart,
    about,
    card_detail,
    add_to_cart,
    increment_cart_item,
    decrement_cart_item,
    remove_cart_item,
)

urlpatterns = [
    path("", landing_page, name="landing"),
    path("home/", home, name="home"),
    path("cart/", view_cart, name="cart"),
    path("about/", about, name="about"),
    path("card_detail/<int:prod_id>", card_detail, name="card_detail"),
    path("add_to_cart/<int:product_id>", add_to_cart, name="add_to_cart"),
    path(
        "increment_cart_item/<int:cart_item_id>",
        increment_cart_item,
        name="incrementar",
    ),
    path(
        "decrement_cart_item/<int:cart_item_id>",
        decrement_cart_item,
        name="decrementar",
    ),
    path("remove_cart_item/<int:cart_item_id>", remove_cart_item, name="remove"),
]
