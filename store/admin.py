from django.contrib import admin
from .models import Category, Product, Order, OrderItem, SoupKit, SoupKitIngredient

# Inline for SoupKitIngredient
class SoupKitIngredientInline(admin.TabularInline):
    model = SoupKitIngredient
    extra = 1
    fields = ['product', 'quantity']
    autocomplete_fields = ['product']  # Optional: Adds search box if many products

# Admin for SoupKit with inline ingredients
@admin.register(SoupKit)
class SoupKitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ['name']
    inlines = [SoupKitIngredientInline]

# Product admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity']
    search_fields = ['name']
    list_filter = ['category']

# Order admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_customer_name', 'created_at', 'total_price', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']

    def get_customer_name(self, obj):
        return obj.user.username
    get_customer_name.short_description = 'Customer Name'

# OrderItem admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']

# Category admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
