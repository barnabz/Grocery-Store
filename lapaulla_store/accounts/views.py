from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from store.models import Wallet

def test_csrf(request):
    return render(request, 'accounts/test_csrf.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('account:login')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
        wallet_balance = wallet.balance
    except Wallet.DoesNotExist:
        wallet_balance = 0.00
    context = {
        'wallet_balance': wallet_balance
    } 
    return render(request, 'accounts/profile.html', context)
