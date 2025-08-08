# sales/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Customer
from products.views import CompanyFilteredMixin # Reutilizamos o mixin para filtrar por empresa

# --- Views para Clientes (Customer) ---

class CustomerListView(LoginRequiredMixin, CompanyFilteredMixin, ListView):
    """
    Lista todos os clientes da empresa do usuário logado.
    """
    model = Customer
    template_name = 'sales/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

class CustomerCreateView(LoginRequiredMixin, CompanyFilteredMixin, CreateView):
    """
    Cria um novo cliente para a empresa do usuário logado.
    """
    model = Customer
    template_name = 'sales/customer_form.html'
    fields = ['name', 'cpf_cnpj', 'email', 'phone', 'address', 'city', 'state', 'zip_code']
    success_url = reverse_lazy('sales:customer_list')

class CustomerUpdateView(LoginRequiredMixin, CompanyFilteredMixin, UpdateView):
    """
    Atualiza um cliente existente da empresa do usuário logado.
    """
    model = Customer
    template_name = 'sales/customer_form.html'
    fields = ['name', 'cpf_cnpj', 'email', 'phone', 'address', 'city', 'state', 'zip_code']
    success_url = reverse_lazy('sales:customer_list')

class CustomerDeleteView(LoginRequiredMixin, CompanyFilteredMixin, DeleteView):
    """
    Exclui um cliente da empresa do usuário logado.
    """
    model = Customer
    template_name = 'sales/customer_confirm_delete.html'
    success_url = reverse_lazy('sales:customer_list')