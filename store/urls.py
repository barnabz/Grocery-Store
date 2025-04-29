from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView  # Import LoginView
from . import views # Import views from the current directory
from .views import (
    HomeView, cart_view, WalletView, ProfileView, OrdersView,
    checkout, add_to_cart, order_success, register_view, order_history,
    update_cart_item, remove_from_cart, deposit_funds,  # Import the deposit_funds view
    soup_kit_list, soup_kit_detail 
)
from .forms import LoginForm, DepositForm  # Import your DepositForm

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cart/', cart_view, name='cart'),
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('checkout/', checkout, name='checkout'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('order-success/', order_success, name='order_success'),
    path('register/', register_view, name='register'),
    path('order-history/', order_history, name='order_history'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('store:home')), name='logout'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('login/', LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm), name='login'),
    path('wallet/deposit/', deposit_funds, name='deposit_funds'),
    path('soup-kits/', soup_kit_list, name='soup_kit_list'),
    path('soup-kits/<int:pk>/', soup_kit_detail, name='soup_kit_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.search_view, name='search'),
    path('category/<slug:slug>/', views.category_detail, name='category'),]
