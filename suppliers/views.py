from django.contrib import messages
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
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

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        filter_by = self.request.GET.get('filter_by', 'name')   
        
        if query and filter_by:
            filter_map = {
                'name': 'name__icontains',
                'cnpj': 'cnpj__icontains',
            }

            filter_param = filter_map.get(filter_by, 'name__icontains')
            queryset = queryset.filter(Q(**{filter_param: query}))

        return queryset

        

class SupplierCreateView(LoginRequiredMixin, CompanyFilteredMixin, CreateView):
    """
    View para criar um novo fornecedor.
    Associa o novo fornecedor à empresa do usuário logado.
    """
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier_list')

    def get_context_data(self, **kwargs):
        """Adiciona uma variável de contexto para indicar que é uma view de criação."""
        context = super().get_context_data(**kwargs)
        context['is_create_view'] = True
        return context

    def form_valid(self, form):
        # Associa o fornecedor à empresa do usuário antes de salvar
        company_user = self.request.user.company_links.filter(active=True).first()
        if company_user:
            form.instance.company = company_user.company
        return super().form_valid(form)


class SupplierUpdateView(LoginRequiredMixin, CompanyFilteredMixin, UpdateView):
    """
    View para editar um fornecedor existente.
    """
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers:supplier_list')

    def get_context_data(self, **kwargs):
        """Adiciona uma variável de contexto para indicar que NÃO é uma view de criação."""
        context = super().get_context_data(**kwargs)
        context['is_create_view'] = False
        return context


class SupplierDeleteView(LoginRequiredMixin, CompanyFilteredMixin, DeleteView):
    """
    View para confirmar a exclusão de um fornecedor.
    """
    model = Supplier
    template_name = 'suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('suppliers:supplier_list')

    def form_valid(self, form):
        # self.object já está definido antes de form_valid ser chamado em DeleteView
        self.object = self.get_object()
        supplier_name = self.object.name
        self.object.delete()
        messages.success(self.request, f'O fornecedor "{supplier_name}" foi excluída com sucesso.')
        return HttpResponseRedirect(self.get_success_url())


class SupplierDetailView(LoginRequiredMixin, CompanyFilteredMixin, DetailView):
    """
    View para exibir os detalhes de um único fornecedor.
    """
    model = Supplier
    template_name = 'suppliers/supplier_detail.html'
    context_object_name = 'supplier'