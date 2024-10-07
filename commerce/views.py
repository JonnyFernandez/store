from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Cart, CartItem, Product

from django.contrib.auth.decorators import login_required


def add_to_cart(request, product_id):
    # Verifica si el usuario está autenticado
    if not request.user.is_authenticated:
        return redirect("login")  # Redirige a la página de login si no está autenticado

    # Busca el producto a agregar al carrito
    product = get_object_or_404(Product, id=product_id)

    # Intenta obtener el carrito del usuario, si no existe, lo crea
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Comprueba si el producto ya está en el carrito
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # Si el producto ya estaba en el carrito, aumenta la cantidad
        cart_item.quantity += 1
    else:
        # Si es la primera vez que se agrega, la cantidad será 1
        cart_item.quantity = 1

    # Guarda el CartItem en la base de datos
    cart_item.save()

    # Redirige a la misma página o al carrito
    return redirect("home")  # 'cart' debe ser la URL del carrito


# Vista para mostrar los productos en el carrito
def view_cart(request):
    # Verifica si el usuario está autenticado
    if not request.user.is_authenticated:
        return redirect("login")

    # Obtiene el carrito del usuario
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Obtiene todos los items del carrito
    cart_items = CartItem.objects.filter(cart=cart)

    context = {
        "cart_items": cart_items,
        "cart": cart,  # Puedes mostrar detalles del carrito como el total
    }
    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "cart": cart,
        },
    )


# Vista para incrementar la cantidad de un producto en el carrito
def increment_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart")


# Vista para disminuir la cantidad de un producto en el carrito
def decrement_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Elimina el item si la cantidad llega a 0
    return redirect("cart")


# Vista para eliminar un producto del carrito
def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()  # Elimina el producto del carrito
    return redirect("cart")


def landing_page(req):
    prod = Product.objects.filter(oferta=True)
    return render(req, "home.html", {"prod": prod})


def home(req):
    prod = Product.objects.all()
    return render(req, "home.html", {"prod": prod})


def about(req):
    return HttpResponse("about")


def card_detail(req, prod_id):
    prod_detail = get_object_or_404(Product, pk=prod_id)
    return render(req, "prod_detail.html", {"detail": prod_detail})
