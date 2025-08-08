from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin # Para exigir login
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from app.mixins import CompanyFilteredMixin

from . import models, forms
from core.models import Company # Importamos Company para filtrar por empresa

# --- Views para Marcas (Brand) ---

class BrandListView(LoginRequiredMixin, CompanyFilteredMixin, ListView):
    model = models.Brand
    template_name = 'products/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 10 

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(name__icontains=query)
        return qs.order_by('name')

class BrandCreateView(LoginRequiredMixin, CompanyFilteredMixin, CreateView):
    model = models.Brand
    template_name = 'products/brand_form.html'
    form_class = forms.BrandForm 
    #success_url = reverse_lazy('products:brand_list') # Redireciona para a lista após criar

    def form_valid(self, form):
        response = super().form_valid(form)

        # Detecta se o formulário foi aberto como um pop-up (ex: `?popup=1` na URL)
        if self.request.GET.get('popup'):
            return HttpResponse(
                '<script>window.opener.location.reload(); window.close();</script>'
            )
        return response

    def get_success_url(self):
        return reverse_lazy('products:brand_list')

    
class BrandUpdateView(LoginRequiredMixin, CompanyFilteredMixin, UpdateView):
    model = models.Brand
    template_name = 'products/brand_form.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('products:brand_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Detecta se o formulário foi aberto como um pop-up (ex: `?popup=1` na URL)
        if self.request.GET.get('popup'):
            return HttpResponse(
                '<script>window.opener.location.reload(); window.close();</script>'
            )
        return response

    def get_success_url(self):
        return reverse_lazy('products:brand_list')


class BrandDeleteView(LoginRequiredMixin, CompanyFilteredMixin, DeleteView):
    model = models.Brand
    template_name = 'products/brand_confirm_delete.html'
    success_url = reverse_lazy('products:brand_list')

    def form_valid(self, form):
        # self.object já está definido antes de form_valid ser chamado em DeleteView
        self.object = self.get_object()
        brand_name = self.object.name
        self.object.delete()
        messages.success(self.request, f'A marca "{brand_name}" foi excluída com sucesso.')
        return HttpResponseRedirect(self.get_success_url())

    


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

    def form_valid(self, form):
        response = super().form_valid(form)

        # Detecta se o formulário foi aberto como um pop-up (ex: `?popup=1` na URL)
        if self.request.GET.get('popup'):
            return HttpResponse(
                '<script>window.opener.location.reload(); window.close();</script>'
            )
        return response

    def get_success_url(self):
        return reverse_lazy('products:category_list')


class CategoryUpdateView(LoginRequiredMixin, CompanyFilteredMixin, UpdateView):
    model = models.Category
    template_name = 'products/category_form.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('products:category_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Detecta se o formulário foi aberto como um pop-up (ex: `?popup=1` na URL)
        if self.request.GET.get('popup'):
            return HttpResponse(
                '<script>window.opener.location.reload(); window.close();</script>'
            )
        return response


class CategoryDeleteView(LoginRequiredMixin, CompanyFilteredMixin, DeleteView):
    model = models.Category
    template_name = 'products/category_confirm_delete.html'
    success_url = reverse_lazy('products:category_list')

    def form_valid(self, form):
        # self.object já está definido antes de form_valid ser chamado em DeleteView
        self.object = self.get_object()
        brand_name = self.object.name
        self.object.delete()
        messages.success(self.request, f'A marca "{brand_name}" foi excluída com sucesso.')
        return HttpResponseRedirect(self.get_success_url())
    
    
# --- Views para Produtos (Product) ---
class ProductListView(LoginRequiredMixin, CompanyFilteredMixin, ListView):
    model = models.Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        # Chama o queryset padrão
        queryset = super().get_queryset()

        # Obtém os parâmetros da URL
        query = self.request.GET.get('q')
        filter_by = self.request.GET.get('filter_by')

        # Se a pesquisa e o filtro existirem, filtra os produtos
        if query and filter_by:
            # Dicionário para mapear os valores do select aos campos do modelo
            filter_map = {
                'name': 'name__icontains',
                'brand': 'brand__name__icontains',
                'category': 'category__name__icontains',
                'sku': 'sku__icontains',
            }

            # Obtém o parâmetro de filtro, com 'name__icontains' como padrão
            filter_param = filter_map.get(filter_by, 'name__icontains')

            # Filtra o queryset usando a busca dinâmica
            queryset = queryset.filter(
                Q(**{filter_param: query})
            )

        # Retorna o queryset final, que pode ou não estar filtrado
        return queryset


class ProductCreateView(LoginRequiredMixin, CompanyFilteredMixin, CreateView):
    model = models.Product
    template_name = 'products/product_form.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('products:product_list')

    # Sobrescrevemos get_form_kwargs para passar o request para o formulário
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = False
        return context

class ProductUpdateView(LoginRequiredMixin, CompanyFilteredMixin, UpdateView):
    model = models.Product
    template_name = 'products/product_form.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('products:product_list')
    
    # Sobrescrevemos get_form_kwargs para passar o request para o formulário
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class ProductDeleteView(LoginRequiredMixin, CompanyFilteredMixin, DeleteView):
    model = models.Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        # self.object já está definido antes de form_valid ser chamado em DeleteView
        self.object = self.get_object()
        brand_name = self.object.name
        self.object.delete()
        messages.success(self.request, f'A marca "{brand_name}" foi excluída com sucesso.')
        return HttpResponseRedirect(self.get_success_url())