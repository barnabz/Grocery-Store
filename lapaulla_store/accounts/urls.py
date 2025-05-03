from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('test_csrf/', views.test_csrf, name='test_csrf'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    # path("dashboard/", views.dashboard, name="dashboard"), 
    # path('test_csrf/', views.test_csrf, name='test_csrf')  # Add this line
]