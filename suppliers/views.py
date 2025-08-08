from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Supplier
from .forms import SupplierForm
from app.mixins import CompanyFilteredMixin # Assumindo a mixin personalizada

class SupplierListView(LoginRequiredMixin, CompanyFilteredMixin, ListView):
    """
    View para listar todos os fornecedores associados à empresa do usuário logado.
    """
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10

class SupplierCreateView(LoginRequiredMixin, CompanyFilteredMixin, CreateView):
    """
    View para criar um novo fornecedor.
    Associa o novo fornecedor à empresa do usuário logado.
    """
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier_list')

    def form_valid(self, form):
        # Associa o fornecedor à empresa do usuário antes de salvar
        form.instance.company = self.request.user.company
        return super().form_valid(form)

class SupplierUpdateView(LoginRequiredMixin, CompanyFilteredMixin, UpdateView):
    """
    View para editar um fornecedor existente.
    """
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier_list')

    def get_queryset(self):
        # Garante que o usuário só pode editar fornecedores da sua empresa
        queryset = super().get_queryset()
        return queryset.filter(company=self.request.user.company)
