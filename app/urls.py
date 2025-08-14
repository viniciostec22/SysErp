from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # Incluímos as URLs de autenticação do Django.
    # Elas vêm com views para login, logout, password reset, etc.
    # Por padrão, as URLs de password reset são:
    # /password_reset/
    # /password_reset/done/
    # /reset/<uidb64>/<token>/
    # /reset/done/
    path('accounts/', include('django.contrib.auth.urls')),
    path('products/', include('products.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('customers/', include('customers.urls')),
    path('stock/', include('stock.urls')),
    path('purchases/', include('purchases.urls')),
    # path('sales/', include('sales.urls')),
    
]
