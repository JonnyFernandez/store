from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from user.models import UserProfile
from .models import AppProduct, Order, OrderItem, Cart, CartItem
from django.http import HttpResponse
from .forms import PostForm, CategoryForm, SearchForm

# para envio de reseñas al email
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.decorators import login_required


# ------------------Home-----------------
def home(request):
    product = AppProduct.objects.all()

    # Verificar si hay una búsqueda
    search_form = SearchForm(request.GET or None)

    if search_form.is_valid():
        name = search_form.cleaned_data.get("name")
        category = search_form.cleaned_data.get("category")

        # Filtrar por nombre
        if name:
            product = product.filter(name__icontains=name)
            if len(product) == 0:
                product = AppProduct.objects.all()

        # Filtrar por categoría
        if category:
            product = product.filter(category=category)

    return render(
        request, "home.html", {"product": product, "search_form": search_form}
    )


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
    if not request.user.is_authenticated:
        return redirect("login")
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
    return render(req, "landing.html", {"product": prod})

def contact_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Personalizar el mensaje
        custom_message = f"""
        ¡Hola! Has recibido una nueva consulta desde tu sitio web.

        Detalles de la consulta:
        ------------------------
        Correo del cliente: {email}
        Mensaje:
        {message}

        Responde directamente a este correo para ponerte en contacto con el cliente.
        """

        # Enviar correo
        send_mail(
            subject=f"Consulta de {email}",  # Asunto del correo
            message=custom_message,  # Mensaje personalizado
            from_email=settings.DEFAULT_FROM_EMAIL,  # Remitente
            recipient_list=["arcancode@gmail.com"],  # Tu correo
            fail_silently=False,  # No fallar en silencio
        )
        return redirect("home")  # Redirigir a una página de agradecimiento

    return render(request, "home.html")


# --------------------------------------------------- a d m i n ---------------------------------------------

@login_required
def orders_pending(request):
    orders = Order.objects.filter(is_pending=True)
    return render(request, "orders_admin.html", {"orders": orders})

@login_required
def order_detail_admin(request, order_id):
    # Obtener la orden solicitada
    order_detail = get_object_or_404(Order, pk=order_id)

    # Acceder directamente al usuario desde la orden
    user = order_detail.user

    # Obtener el perfil del usuario
    user_profile = UserProfile.objects.get(
        user=user
    )  # user ya es una instancia del modelo User

    print(user)

    # Obtener los ítems de la orden
    order_items = OrderItem.objects.filter(order=order_detail).select_related("product")

    return render(
        request,
        "order_detail.html",
        {
            "order": order_detail,
            "order_items": order_items,  # Incluir los productos en la orden
            "user_profile": user_profile,  # Agregar el perfil del usuario al contexto
        },
    )

@login_required
def orders_dispatch(request):
    orders = Order.objects.filter(is_pending=False)
    return render(request, "orders_admin.html", {"orders": orders})

@login_required
def add_product(request):
    if request.method == "GET":
        return render(
            request,
            "add_prod.html",
            {
                "form": PostForm(),  # Formulario de producto
                "form2": CategoryForm(),  # Formulario de categoría
            },
        )
    else:
        form = PostForm(request.POST, request.FILES)
        form2 = CategoryForm(request.POST)

        product_saved = False
        category_saved = False

        # Si el formulario de producto es válido, guarda el producto
        if form.is_valid():
            new_prod = form.save(commit=False)
            new_prod.user = (
                request.user
            )  # Asigna el usuario que está creando el producto
            new_prod.save()
            product_saved = True

        # Si el formulario de categoría es válido, guarda la categoría
        if form2.is_valid():
            new_category = form2.save()
            category_saved = True

        # Redirigir si al menos uno de los formularios fue guardado
        if product_saved:
            return redirect("home")
        elif category_saved:
            return redirect("add_product")
        else:
            return redirect("add_product")

        # Si ninguno fue guardado, se devuelven los formularios con los errores correspondientes
        return render(
            request,
            "add_prod.html",
            {
                "form": form,
                "form2": form2,
                "error": "Ingresar datos válidos en el formulario correspondiente.",
            },
        )

@login_required
def add_category(request):
    if request.method == "POST":
        form2 = CategoryForm(request.POST)
        if form2.is_valid():
            form2.save()
            return redirect(
                "add_category"
            )  # Redirigir si la categoría se guarda correctamente
        else:
            return render(
                request,
                "add_category.html",
                {
                    "form2": form2,
                    "error": "Ingresar datos válidos en el formulario correspondiente.",
                },
            )
    else:
        # Mostrar el formulario vacío cuando el método es GET
        return render(
            request,
            "add_category.html",
            {
                "form2": CategoryForm(),
            },
        )

@login_required
def product_detail_admin(request, prod_id):
    prod = get_object_or_404(AppProduct, pk=prod_id)

    if request.method == "GET":
        form = PostForm(instance=prod)
        return render(request, "prod_detail_admin.html", {"prod": prod, "form": form})

    else:
        form = PostForm(request.POST, request.FILES, instance=prod)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(
                request,
                "prod_detail_admin.html",
                {"prod": prod, "form": form, "error": "Error en la actualización"},
            )

@login_required
def delete_prod(request, prod_id):
    prod = get_object_or_404(AppProduct, pk=prod_id)

    if request.method == "POST":
        prod.delete()
        return redirect("home")

@login_required
def aproff_order(request, order_id):
    # Obtenemos la orden específica
    order = get_object_or_404(Order, pk=order_id)

    if request.method == "POST":
        # Cambiamos el estado de la orden a "no pendiente"
        order.is_pending = False
        order.save()

        # Iteramos sobre los productos en la orden y actualizamos el stock
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            product = item.product
            # Restamos la cantidad pedida del stock
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()  # Guardamos los cambios en el producto
            else:
                # Si no hay suficiente stock, podrías manejar un mensaje de error
                return render(
                    request,
                    "order_detail.html",
                    {
                        "order": order,
                        "error": f"No hay suficiente stock para {product.name}",
                    },
                )

        # Redirigir a una página de éxito o a la lista de órdenes
        return redirect("orders_dispatch")

    return render(request, "order_detail.html", {"order": order})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == "POST":
        order.delete()
        return redirect("orders_pending")


def about(request):
    return render(request, "about.html", {})
