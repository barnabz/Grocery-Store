from django.shortcuts import render, redirect, get_object_or_404
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
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"Added {product.name} to cart.")
    return redirect('store:home')



@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    total = 0
    for item in cart.items.all():
        if isinstance(item.product, SoupKit):
            total += item.product.price  # Use the SoupKit's price
        else:
            total += item.product.price * item.quantity
    return render(request, 'store/cart.html', {
        'cart': cart,
        'total': total,
        'wallet_balance': Wallet.objects.get(user=request.user).balance
    })

@require_POST
@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')

    if action == 'increment':
        item.quantity += 1
        item.save()
    elif action == 'decrement':
        item.quantity -= 1
        if item.quantity < 1:
            item.delete()
        else:
            item.save()
    return redirect('store:cart')


@require_POST
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, f"Removed {item.product.name} from cart.")
    return redirect('store:cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    wallet = Wallet.objects.get(user=request.user)
    total = 0
    for item in cart.items.all():
        if isinstance(item.product, SoupKit):
            total += item.product.price
        else:
            total += item.product.price * item.quantity

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        use_wallet = request.POST.get('use_wallet') == 'on'

        if use_wallet and wallet.balance >= total:
            wallet.balance -= total
            wallet.save()
            paid_from_wallet = True
        elif use_wallet:
            messages.error(request, "Insufficient wallet balance.")
            return redirect('store:checkout')
        else:
            messages.info(request, "Payment gateway integration needed.")
            return redirect('store:checkout')

        order = Order.objects.create(
            user=request.user,
            total_price=total,
            shipping_address=shipping_address,
            paid_from_wallet=paid_from_wallet
        )
        for item in cart.items.all():
             if isinstance(item.product, SoupKit):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=1, # set quantity to 1 for soup kit
                    price=item.product.price
                )
             else:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
        cart.items.all().delete()
        messages.success(request, "Order placed successfully!")
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
