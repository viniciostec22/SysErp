from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # URLs para Clientes
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<uuid:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<uuid:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
]