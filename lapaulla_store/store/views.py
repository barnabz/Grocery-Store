from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.views.generic import ListView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Product, Category, Cart, CartItem, Wallet, Order, OrderItem, SoupKit  # Import SoupKit
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DepositForm  # Import your DepositForm

class HomeView(ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['soup_kits'] = SoupKit.objects.all()
        context['categories'] = Category.objects.all()
        print(f"Context in HomeView: {context}")
        if self.request.user.is_authenticated:
            wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            context['wallet_balance'] = wallet.balance
            context['cart_item_count'] = cart.items.count()
        else:
            context['wallet_balance'] = None
            context['cart_item_count'] = 0
        return context

def search_view(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'store/search_results.html', {'results': results, 'query': query})


    def get_queryset(self):
        queryset = Product.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['soup_kits'] = SoupKit.objects.all()  # Get all soup kits
        if self.request.user.is_authenticated:
            wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            context['wallet_balance'] = wallet.balance
            context['cart_item_count'] = cart.items.count()
        else:
            context['wallet_balance'] = None
            context['cart_item_count'] = 0
        return context

class OrdersView(TemplateView):
    template_name = 'store/orders.html'

class WalletView(LoginRequiredMixin, TemplateView):
    template_name = 'store/wallet.html'
    login_url = '/login/'  # Redirect to login if not authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            wallet = Wallet.objects.get(user=self.request.user)
            context['wallet_balance'] = wallet.balance
        except Wallet.DoesNotExist:
            context['wallet_balance'] = 0  # Or handle the case as needed
        return context

class ProfileView(TemplateView):
    template_name = 'store/profile.html'



def soup_kit_list(request):
    soup_kits = SoupKit.objects.all()
    return render(request, 'store/soup_kit_list.html', {'soup_kits': soup_kits})

def soup_kit_detail(request, pk):
    soup_kit = get_object_or_404(SoupKit, pk=pk)
    return render(request, 'store/soup_kit_detail.html', {'soup_kit': soup_kit})



@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not product.available or product.stock_quantity < 1:
        messages.error(request, "This product is currently unavailable.")
        return redirect('store:home')

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        if cart_item.quantity >= product.stock_quantity:
            messages.error(request, "Not enough stock available.")
            return redirect('store:home')

        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Added {product.name} to cart.")
    return redirect('store:home')

@login_required
@require_POST
def add_soup_kit_to_cart(request, soup_kit_id):
    soup_kit = get_object_or_404(SoupKit, id=soup_kit_id)

    if not soup_kit.available or soup_kit.stock_quantity < 1:
        messages.error(request, "This soup kit is currently unavailable.")
        return redirect('store:home')

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        soup_kit=soup_kit,
        defaults={'quantity': 1}
    )

    if not created:
        if cart_item.quantity >= soup_kit.stock_quantity:
            messages.error(request, "Not enough soup kit stock available.")
            return redirect('store:home')

        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Added {soup_kit.name} to cart.")
    return redirect('store:home')
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    wallet, _ = Wallet.objects.get_or_create(user=request.user)

    return render(request, 'store/cart.html', {
        'cart': cart,
        'total': cart.total_price(),
        'wallet_balance': wallet.balance,
    })


@require_POST
@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    try:
        quantity = int(request.POST.get('quantity', ''))
    except (ValueError, TypeError):
        messages.error(request, "Please enter a valid quantity.")
        return redirect('store:cart')

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect('store:cart')

    product = item.product or item.soup_kit

    if quantity > product.stock_quantity:
        messages.error(request, "Requested quantity exceeds available stock.")
        return redirect('store:cart')

    item.quantity = quantity
    item.save()

    messages.success(request, "Cart updated successfully.")
    return redirect('store:cart')


@require_POST
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item_name = item.product.name if item.product else item.soup_kit.name
    item.delete()

    messages.info(request, f"Removed {item_name} from cart.")
    return redirect('store:cart')


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = list(cart.items.select_related('product', 'soup_kit'))
    total = cart.total_price()
    wallet, _ = Wallet.objects.get_or_create(user=request.user)

    if not cart_items:
        messages.info(request, "Your cart is empty.")
        return redirect('store:cart')

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address', '').strip()
        use_wallet = request.POST.get('use_wallet') == 'on'

        if not shipping_address:
            messages.error(request, "Please enter your shipping address.")
            return redirect('store:checkout')

        if not use_wallet:
            messages.info(
                request,
                "Wallet payment is currently the available simulated payment option."
            )
            return redirect('store:checkout')

        try:
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(
                    user=request.user
                )

                if wallet.balance < total:
                    raise ValueError("Insufficient wallet balance.")

                checked_items = []

                for item in cart_items:
                    if item.product_id:
                        catalog_item = Product.objects.select_for_update().get(
                            pk=item.product_id
                        )
                        product = catalog_item
                        soup_kit = None
                    else:
                        catalog_item = SoupKit.objects.select_for_update().get(
                            pk=item.soup_kit_id
                        )
                        product = None
                        soup_kit = catalog_item

                    if not catalog_item.available:
                        raise ValueError(
                            f"{catalog_item.name} is currently unavailable."
                        )

                    if catalog_item.stock_quantity < item.quantity:
                        raise ValueError(
                            f"Insufficient stock for {catalog_item.name}."
                        )

                    checked_items.append(
                        (item, catalog_item, product, soup_kit)
                    )

                order = Order.objects.create(
                    user=request.user,
                    total_price=total,
                    shipping_address=shipping_address,
                    paid_from_wallet=True
                )

                for item, catalog_item, product, soup_kit in checked_items:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        soup_kit=soup_kit,
                        item_name=catalog_item.name,
                        quantity=item.quantity,
                        price=catalog_item.price
                    )

                    catalog_item.stock_quantity -= item.quantity
                    catalog_item.save(update_fields=['stock_quantity'])

                wallet.balance -= total
                wallet.save(update_fields=['balance', 'updated_at'])

                cart.items.all().delete()

        except ValueError as error:
            messages.error(request, str(error))
            return redirect('store:checkout')

        messages.success(request, "Your order was placed successfully!")
        return redirect('store:order_success')

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'total': total,
        'wallet_balance': wallet.balance
    })
def order_success(request):
    return render(request, 'store/order_success.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Account created for {username}!")
            return redirect('store:home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def deposit_funds(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            # In a real application, you would integrate with a payment gateway here
            # For this example, we'll just simulate a successful deposit

            wallet = Wallet.objects.get(user=request.user)
            wallet.balance += amount
            wallet.save()

            messages.success(request, f"₦{amount:.2f} deposited successfully!")
            return redirect('store:wallet')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DepositForm()
    return render(request, 'store/deposit.html', {'form': form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products,
    })
