# sales/views.py

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Customer
from . import forms
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

class CustomerCreateView(CreateView):
    model = Customer
    form_class = forms.CustomerForm
    template_name = 'sales/customer_form.html'
    success_url = reverse_lazy('sales:customer_list')

    def form_valid(self, form):
        """
        Adiciona a empresa do usuário logado à instância do cliente
        antes de salvar o formulário, usando a relação CompanyUser.
        """
        try:
            # Obtém a primeira empresa associada ao usuário logado
            company_user = self.request.user.company_links.first()
            if company_user:
                form.instance.company = company_user.company
            else:
                # Caso o usuário não esteja associado a nenhuma empresa
                # Você pode adicionar um tratamento de erro mais robusto aqui
                # como um raise e um redirect para uma página de erro
                # print("Erro: O usuário logado não tem uma empresa associada.")
                pass
        except AttributeError:
            # print("Erro: Acesso à relação CompanyUser falhou.")
            pass
        messages.success(self.request, "Cliente cadastrado com sucesso.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'sales/customer_detail.html'
    context_object_name = 'customer'

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = forms.CustomerForm
    template_name = 'sales/customer_form.html'
    success_url = reverse_lazy('sales:customer_list')

    def form_valid(self, form):
        """
        Adiciona a empresa do usuário logado à instância do cliente
        antes de salvar o formulário, usando a relação CompanyUser.
        """
        try:
            # Obtém a primeira empresa associada ao usuário logado
            company_user = self.request.user.company_links.first()
            if company_user:
                form.instance.company = company_user.company
            else:
                # print("Erro: O usuário logado não tem uma empresa associada.")
                pass
        except AttributeError:
            # print("Erro: Acesso à relação CompanyUser falhou.")
            pass
        messages.success(self.request, "Cliente atualizado com sucesso.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class CustomerDeleteView(LoginRequiredMixin, CompanyFilteredMixin, DeleteView):
    """
    Exclui um cliente da empresa do usuário logado.
    """
    model = Customer
    template_name = 'sales/customer_confirm_delete.html'
    success_url = reverse_lazy('sales:customer_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cliente excluído com sucesso.")
        return super().delete(request, *args, **kwargs)
