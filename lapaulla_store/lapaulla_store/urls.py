from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.views import HomeView, OrdersView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('store/', include('store.urls', namespace='store')),  # Include store URLs under /store/
    path('logout/', LogoutView.as_view(), name='logout'),
    path("account/", include("accounts.urls", namespace="account")),  # Add this line!
]

# Add static file serving for development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Keep media file serving as it was
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)