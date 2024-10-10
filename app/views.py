from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from user.models import UserProfile
from .models import AppProduct, Order, OrderItem, Cart, CartItem
from django.http import HttpResponse
from django.contrib.auth.models import User


# ------------------Home-----------------
def home(request):
    product = AppProduct.objects.all()
    return render(request, "home.html", {"product": product})


def add_to_cart(request, prod_id):

    if not request.user.is_authenticated:
        return redirect("login")

    product = get_object_or_404(AppProduct, id=prod_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    # if not cart:
    #     return redirect("home")

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity = cart_item.quantity
    else:
        cart_item.quantity = 1

    cart_item.save()

    return redirect("home")


def cart(request):
    if not request.user.is_authenticated:
        return redirect("login")
    try:
        cart = get_object_or_404(Cart, user=request.user)
    except:
        error = "Carrito Vacio"
        return render(request, "cart.html", {"error": error})

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None  # Maneja el caso en que el perfil no existe

    # Obtener los ítems del carrito
    cart_items = cart.cartitem_set.all()

    # Calcular el costo total del carrito
    total_cost = cart.get_total_cost()

    context = {
        "cart": cart,
        "user_profile": user_profile,  # Agregar el perfil del usuario al contexto
        "cart_items": cart_items,  # Pasar los ítems del carrito al contexto
        "total_cost": total_cost,
    }

    return render(request, "cart.html", context)


def increment_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart")


def decrement_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Elimina el item si la cantidad llega a 0
    return redirect("cart")


def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()  # Elimina el producto del carrito
    return redirect("cart")


def create_order(request):
    user = request.user
    cart = user.cart  # Obtener el carrito del usuario

    # Obtener el perfil del usuario
    user_profile = get_object_or_404(UserProfile, user=user)

    # Crear la orden
    order = Order.objects.create(
        user=user,
        total_price=cart.get_total_cost(),
        email=user_profile.email,
        tel=user_profile.tel,
        address=user_profile.addres,
    )

    # Transferir los productos del CartItem a OrderItem
    for (
        cart_item
    ) in (
        cart.cartitem_set.all()
    ):  # Cambiado de cart.items.all() a cart.cartitem_set.all()
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,  # Acceder al producto desde CartItem
            quantity=cart_item.quantity,  # Cantidad en CartItem
            price=cart_item.product.price,  # Precio actual del producto
        )

    # Vaciar el carrito (opcional)
    cart.items.clear()

    return redirect("purchases")


def purchases(request):
    # Intentar obtener el perfil del usuario
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None  # Maneja el caso en que el perfil no existe
    all_order = Order.objects.filter(user=request.user)
    if not all_order:
        res = "No Tienes Ordenes de compra registradas"
        return render(
            request, "purchase.html", {"user_profile": user_profile, "error": res}
        )
    else:
        return render(
            request,
            "purchase.html",
            {
                "orders": all_order,
                "user_profile": user_profile,
            },
        )


def order_detail(request, order_id):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None  # Maneja el caso en que el perfil no existe
        print(user_profile)

    # Obtener la orden solicitada
    order_detail = get_object_or_404(Order, pk=order_id, user=request.user)

    # Obtener los items de la orden (relacionados a través de OrderItem)
    order_items = OrderItem.objects.filter(order=order_detail).select_related("product")

    return render(
        request,
        "order_detail.html",
        {
            "order": order_detail,
            "order_items": order_items,  # Incluir los productos en la orden
            "user_profile": user_profile,
        },
    )


def card_detail(req, prod_id):
    prod_detail = get_object_or_404(AppProduct, pk=prod_id)
    return render(req, "prod_detail.html", {"detail": prod_detail})


def landing_page(req):
    prod = AppProduct.objects.filter(offer=True)
    return render(req, "home.html", {"product": prod})
