from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from cloudinary.models import CloudinaryField

# Create your models here.


# -----------------------------------------------Categoria-------------------------
class AppCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# -----------------------------------------------Producto-------------------------
class AppProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    imagen = CloudinaryField(
        "image",
        blank=True,
        null=True,
        transformation={
            "width": 400,  # Ancho deseado
            "height": 400,  # Alto deseado
            "crop": "fill",  # Recortar y rellenar para que se ajuste al tamaño
            "gravity": "auto",  # Enfocar en la parte más importante de la imagen
        },
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], default=1
    )
    stock = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    offer = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(
        AppCategory, on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self):
        return f"{self.name}"


# -----------------------------------------------carrito-------------------------
# -----------------------------------------------carrito-------------------------
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField("AppProduct", through="CartItem")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"

    def get_total_cost(self):
        # Mejor uso de querysets para calcular el total de forma eficiente
        return (
            self.cartitem_set.aggregate(
                total=models.Sum(models.F("quantity") * models.F("product__price"))
            )["total"]
            or 0
        )


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey("AppProduct", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        # Usa directamente el precio del producto
        return self.quantity * self.product.price


# -----------------------------------------------Orden-------------------------
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    items = models.ManyToManyField("AppProduct", through="OrderItem")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_pending = models.BooleanField(default=True)

    # Información del cliente (traída del UserProfile)
    email = models.EmailField()  # Se copia del perfil del usuario
    tel = models.CharField(max_length=20)  # Número de teléfono (de UserProfile)
    address = models.CharField(max_length=255)  # Dirección de envío (de UserProfile)

    def __str__(self):
        return f"Orden {self.id} de {self.user.username}"

    @property
    def total_cost(self):
        # Calcula el total basado en los OrderItems
        return (
            self.orderitem_set.aggregate(
                total=models.Sum(models.F("quantity") * models.F("price"))
            )["total"]
            or 0
        )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("AppProduct", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en orden {self.order.id}"

    def get_total_price(self):
        return self.quantity * self.price
