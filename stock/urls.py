# stock/urls.py
from django.urls import path
from .views import current_stock_list, PurchaseCreateView, SaleCreateView

app_name = 'stock'

urlpatterns = [
    path('', current_stock_list, name='current_stock_list'),
    path('purchase/add/', PurchaseCreateView.as_view(), name='add_purchase'),
    path('sale/add/', SaleCreateView.as_view(), name='add_sale'),
]
