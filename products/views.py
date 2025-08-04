from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin # Para exigir login
from django.contrib import messages
from django.shortcuts import get_object_or_404

from . import models, forms
from core.models import Company # Importamos Company para filtrar por empresa

# Mixin para garantir que apenas dados da empresa do usuário logado sejam acessados
class CompanyFilteredMixin:
    def get_queryset(self):
        print(f"DEBUG: Usuário logado: {self.request.user.email}")
        if self.request.user.is_authenticated and hasattr(self.request.user, 'company_links'): # CORRIGIDO: de 'companyuser_set' para 'company_links'
            # Encontra a CompanyUser ativa para o usuário logado
            # Usamos .all() para acessar o related_manager e depois filtramos
            company_user = self.request.user.company_links.filter(active=True).first()
            if company_user:
                print(f"DEBUG: CompanyUser ativa encontrada: {company_user.user.email} -> {company_user.company.name}")
                queryset = super().get_queryset().filter(company=company_user.company)
                print(f"DEBUG: Quantidade de objetos após filtro da empresa: {queryset.count()}")
                return queryset
            else:
                print("DEBUG: Nenhuma CompanyUser ativa encontrada para o usuário logado.")
        else:
            print("DEBUG: Usuário não autenticado ou sem company_links.") # Mensagem de depuração atualizada
        return self.model.objects.none()

    def form_valid(self, form):
        # AQUI TAMBÉM PRECISAMOS USAR 'company_links'
        if self.request.user.is_authenticated and hasattr(self.request.user, 'company_links'):
            company_user = self.request.user.company_links.filter(active=True).first()
            if company_user:
                form.instance.company = company_user.company
                messages.success(self.request, f"{self.model._meta.verbose_name} salvo com sucesso!")
                return super().form_valid(form)
        messages.error(self.request, "Não foi possível associar o item a uma empresa. Verifique seu perfil.")
        return self.form_invalid(form)


# --- Views para Marcas (Brand) ---

class BrandListView(LoginRequiredMixin, CompanyFilteredMixin, ListView):
    model = models.Brand
    template_name = 'products/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 10 # Opcional: paginar a lista

class BrandCreateView(LoginRequiredMixin, CompanyFilteredMixin, CreateView):
    model = models.Brand
    template_name = 'products/brand_form.html'
    form_class = forms.BrandForm 
    success_url = reverse_lazy('products:brand_list') # Redireciona para a lista após criar

class BrandUpdateView(LoginRequiredMixin, CompanyFilteredMixin, UpdateView):
    model = models.Brand
    template_name = 'products/brand_form.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('products:brand_list')

class BrandDeleteView(LoginRequiredMixin, CompanyFilteredMixin, DeleteView):
    model = models.Brand
    template_name = 'products/brand_confirm_delete.html'
    success_url = reverse_lazy('products:brand_list')

# --- Views para Categorias (Category) ---

class CategoryListView(LoginRequiredMixin, CompanyFilteredMixin, ListView):
    model = models.Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

class CategoryCreateView(LoginRequiredMixin, CompanyFilteredMixin, CreateView):
    model = models.Category
    template_name = 'products/category_form.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('products:category_list')

class CategoryUpdateView(LoginRequiredMixin, CompanyFilteredMixin, UpdateView):
    model = models.Category
    template_name = 'products/category_form.html'
    forms_class = forms.CategoryForm
    success_url = reverse_lazy('products:category_list')

class CategoryDeleteView(LoginRequiredMixin, CompanyFilteredMixin, DeleteView):
    model = models.Category
    template_name = 'products/category_confirm_delete.html'
    success_url = reverse_lazy('products:category_list')