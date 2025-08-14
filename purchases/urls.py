from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    path('', views.PurchaseInvoiceListView.as_view(), name='purchase_list'),
    # path('<uuid:pk>/', views.purchase_detail, name='purchase_detail'),
    path('create/', views.PurchaseInvoiceCreateView.as_view(), name='purchase_create'),
    # path('<uuid:pk>/update/', views.purchase_update, name='purchase_update'),
    # path('<uuid:pk>/delete/', views.purchase_delete, name='purchase_delete'),
 
    # NOVAS APIs para o Select2
    path('api/buscar_fornecedores/', views.buscar_fornecedores, name='buscar_fornecedores'),
    path('api/buscar_produtos/', views.buscar_produtos, name='buscar_produtos'),
]

