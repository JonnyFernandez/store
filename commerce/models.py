from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField


# Productos
class Product(models.Model):
    nombre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    imagen = CloudinaryField("image", blank=True, null=True)
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    oferta = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.nombre


# Carrito
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField(
        "Product", through="CartItem"
    )  # Relación con los productos a través de CartItem
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"

    # Método para calcular el costo total del carrito
    def get_total_cost(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())


# Item del Carrito
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.precio


# Orden (Historial de Compras)
class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )  # Relación de uno a muchos
    items = models.ManyToManyField(
        "Product", through="OrderItem"
    )  # Relación con los productos comprados
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Completed", "Completed")],
        default="Pending",
    )

    def __str__(self):
        return f"Orden {self.id} de {self.user.username}"


# Item de la Orden
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Precio en el momento de la compra

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en orden {self.order.id}"
