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
    create_order,
    purchases,
    # admin
    orders_pending,
    orders_dispatch,
    orders_detail,
    add_product,
    order_detail_admin,
    product_detail_admin,
    delete_prod,
    aproff_order,
    delete_order,
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
    path("create_order/", create_order, name="create_order"),
    path("purchases/", purchases, name="purchases"),
    # admin
    path(
        "order_detail_admin/<int:order_id>",
        order_detail_admin,
        name="order_detail_admin",
    ),
    path("orders_pending/", orders_pending, name="orders_pending"),
    path("orders_dispatch/", orders_dispatch, name="orders_dispatch"),
    path("orders_detail/<int:order_id>", orders_detail, name="orders_detail"),
    path("add_product/", add_product, name="add_product"),
    path(
        "product_detail_admin/<int:prod_id>",
        product_detail_admin,
        name="product_detail_admin",
    ),
    path("delete_prod/<int:prod_id>", delete_prod, name="delete_prod"),
    path("aproff_order/<int:order_id>", aproff_order, name="aproff_order"),
    path("delete_order/<int:order_id>", delete_order, name="delete_order"),
]
