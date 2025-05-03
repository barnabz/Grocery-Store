from django.core.management.base import BaseCommand
from decimal import Decimal
from store.models import Category, Product, SoupKit, SoupKitIngredient

class Command(BaseCommand):
    help = 'Seed database with sample soup kit and condiments'

    def handle(self, *args, **kwargs):
        soup_category, _ = Category.objects.get_or_create(name="Soups")

        ogbono, _ = Product.objects.get_or_create(
            name="Egusi",
            category=soup_category,
            price=Decimal("0.10"),
            stock_quantity=100
        )

        pumpkin, _ = Product.objects.get_or_create(
            name="Red Oil",
            category=soup_category,
            price=Decimal("0.15"),
            stock_quantity=100
        )

        Egusi_soup = SoupKit.objects.create(
            name="Egusi Soup Kit",
            description="A comforting Egusi soup with classic condiments.",
            price=Decimal("7.99"),
            category=soup_category
        )

        SoupKitIngredient.objects.create(soup_kit=Egusi_soup, product= ogbono, quantity=1)
        SoupKitIngredient.objects.create(soup_kit=Egusi_soup, product= pumpkin, quantity=1)

        self.stdout.write(self.style.SUCCESS('Soup kit and condiments created successfully!'))