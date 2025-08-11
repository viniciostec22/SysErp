# customers/views.py
from pyexpat.errors import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.mixins import CompanyFilteredMixin
from .models import Customer
from .forms import CustomerForm

class CustomerListView(LoginRequiredMixin, CompanyFilteredMixin, ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

class CustomerDetailView(LoginRequiredMixin, CompanyFilteredMixin, DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'

class CustomerCreateView(LoginRequiredMixin, CompanyFilteredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:customer_list')

    def get_context_data(self, **kwargs):
        """Adiciona uma variável de contexto para indicar que é uma view de criação."""
        context = super().get_context_data(**kwargs)
        context['is_create_view'] = True
        return context

    def form_valid(self, form):
        try:
            company_user = self.request.user.company_links.first()
            if company_user:
                form.instance.company = company_user.company
            else:
                return self.form_invalid(form)
        except AttributeError:
            return self.form_invalid(form)

        return super().form_valid(form)

class CustomerUpdateView(LoginRequiredMixin, CompanyFilteredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:customer_list')

    def get_context_data(self, **kwargs):
        """Adiciona uma variável de contexto para indicar que é uma view de criação."""
        context = super().get_context_data(**kwargs)
        context['is_create_view'] = False
        return context

    def form_valid(self, form):
        try:
            company_user = self.request.user.company_links.first()
            if company_user:
                form.instance.company = company_user.company
            else:
                messages.success(self.request, 'Customer updated successfully.')
                return self.form_invalid(form)
        except AttributeError:
            return self.form_invalid(form)
        
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, CompanyFilteredMixin, DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customers:customer_list')
