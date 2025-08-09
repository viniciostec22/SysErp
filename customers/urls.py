# customers/urls.py

from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    # URLs para Clientes
    # O caminho vazio ('') corresponde à URL base do app ('customers/')
    path('', views.CustomerListView.as_view(), name='customer_list'),
    path('create/', views.CustomerCreateView.as_view(), name='customer_create'),
    # Usamos <int:pk> pois o ID do cliente é um inteiro
    path('<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
]
