
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import (
    Category,
    Product,
    SoupKit,
    Cart,
    CartItem,
    Wallet,
    Order,
    OrderItem,
)


class GroceryStoreTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testcustomer",
            password="TestPassword123!"
        )

        self.client.login(
            username="testcustomer",
            password="TestPassword123!"
        )

        self.category = Category.objects.create(name="Fresh Meat")

        self.product = Product.objects.create(
            name="Cow Meat",
            category=self.category,
            price=Decimal("7640.00"),
            stock_quantity=10,
            available=True
        )

        self.soup_kit = SoupKit.objects.create(
            name="Egusi Soup Kit",
            description="A complete Egusi soup kit",
            category=self.category,
            price=Decimal("5690.00"),
            stock_quantity=10,
            available=True
        )

        self.wallet = Wallet.objects.create(
            user=self.user,
            balance=Decimal("100000.00")
        )

    def test_add_product_to_cart(self):
        response = self.client.post(
            reverse(
                "store:add_to_cart",
                args=[self.product.id]
            )
        )

        self.assertEqual(response.status_code, 302)

        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product)

    def test_add_soup_kit_to_cart(self):
        response = self.client.post(
            reverse(
                "store:add_soup_kit_to_cart",
                args=[self.soup_kit.id]
            )
        )

        self.assertEqual(response.status_code, 302)

        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().soup_kit, self.soup_kit)

    def test_cart_calculates_combined_total(self):
        cart = Cart.objects.create(user=self.user)

        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        CartItem.objects.create(
            cart=cart,
            soup_kit=self.soup_kit,
            quantity=1
        )

        expected_total = Decimal("20970.00")

        self.assertEqual(cart.total_price(), expected_total)

    def test_successful_wallet_checkout(self):
        cart = Cart.objects.create(user=self.user)

        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        CartItem.objects.create(
            cart=cart,
            soup_kit=self.soup_kit,
            quantity=1
        )

        response = self.client.post(
            reverse("store:checkout"),
            {
                "shipping_address": "Test Delivery Address, Lagos",
                "use_wallet": "on"
            }
        )

        self.assertRedirects(
            response,
            reverse("store:order_success")
        )

        order = Order.objects.get(user=self.user)

        self.assertEqual(order.total_price, Decimal("20970.00"))
        self.assertTrue(order.paid_from_wallet)
        self.assertEqual(order.items.count(), 2)

        self.wallet.refresh_from_db()
        self.product.refresh_from_db()
        self.soup_kit.refresh_from_db()

        self.assertEqual(
            self.wallet.balance,
            Decimal("79030.00")
        )

        self.assertEqual(self.product.stock_quantity, 8)
        self.assertEqual(self.soup_kit.stock_quantity, 9)
        self.assertEqual(cart.items.count(), 0)

    def test_checkout_rejects_insufficient_wallet_balance(self):
        cart = Cart.objects.create(user=self.user)

        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )

        self.wallet.balance = Decimal("100.00")
        self.wallet.save()

        response = self.client.post(
            reverse("store:checkout"),
            {
                "shipping_address": "Test Delivery Address, Lagos",
                "use_wallet": "on"
            }
        )

        self.assertRedirects(
            response,
            reverse("store:checkout")
        )

        self.assertEqual(Order.objects.count(), 0)

        self.wallet.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(self.wallet.balance, Decimal("100.00"))
        self.assertEqual(self.product.stock_quantity, 10)
        self.assertEqual(cart.items.count(), 1)
