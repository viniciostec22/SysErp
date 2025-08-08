from django.urls import path
from . import views

app_name = 'suppliers' # Define um namespace para as URLs da app

urlpatterns = [
    path('', views.SupplierListView.as_view(), name='supplier_list'),
    path('create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('<uuid:pk>/update/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('<uuid:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
 
 
]
