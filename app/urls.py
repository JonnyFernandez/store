from django.urls import path
from .views import (
    home,
    card_detail,
    add_to_cart,
    order_detail,
    increment_cart_item,
    decrement_cart_item,
    remove_cart_item,
    cart,
    landing_page,
)

urlpatterns = [
    path("", landing_page, name="landing"),
    path("home/", home, name="home"),
    path("card_detail/<int:prod_id>", card_detail, name="card_detail"),
    path("add_to_cart/<int:prod_id>", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
    path("order_detail/<int:order_id>", order_detail, name="order_detail"),
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
