from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Category Model (Assuming you have this)
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# Product Model (Assuming you have this)
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock_quantity = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

# Wallet Model
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet: ₦{self.balance}"


#Cart Model

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username if self.user else 'Guest'}"

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        return sum(
            (item.total_price() for item in self.items.all()),
            Decimal("0.00")
        )


# Cart Item Model
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    soup_kit = models.ForeignKey(
        'SoupKit',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(product__isnull=False, soup_kit__isnull=True)
                    | models.Q(product__isnull=True, soup_kit__isnull=False)
                ),
                name='cart_item_exactly_one_type',
            ),
        ]

    def __str__(self):
        item = self.product or self.soup_kit
        return f"{self.quantity} x {item.name}"

    def total_price(self):
        item = self.product or self.soup_kit
        return item.price * self.quantity



# Order Model
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    paid_from_wallet = models.BooleanField(default=False)
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# Order Item Model (Assuming you have this)
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    soup_kit = models.ForeignKey(
        'SoupKit',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    item_name = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(product__isnull=False, soup_kit__isnull=True)
                    | models.Q(product__isnull=True, soup_kit__isnull=False)
                ),
                name='order_item_exactly_one_type',
            ),
        ]

    def __str__(self):
        name = self.item_name or (
            self.product.name if self.product else self.soup_kit.name
        )
        return f"{self.quantity} x {name} in Order {self.order.id}"

# SoupKit Model
class SoupKit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='soup_kits') # Add this
    image = models.ImageField(upload_to='soup_kits/', null=True, blank=True)
    ingredients = models.ManyToManyField(
        Product,
        related_name='soup_kits',
        through='SoupKitIngredient',
        through_fields=('soup_kit', 'product')  # Explicitly define through fields
    )

    def __str__(self):
        return self.name

class SoupKitIngredient(models.Model):
    soup_kit = models.ForeignKey(SoupKit, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('soup_kit', 'product')

    def __str__(self):
        return f"{self.product.name} in {self.soup_kit.name} ({self.quantity})"
