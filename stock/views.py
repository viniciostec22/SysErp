# stock/views.py

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import StockMovement
from products.models import Product
from suppliers.models import Supplier
from customers.models import Customer
from .forms import PurchaseForm, SaleForm


def current_stock_list(request):
    """
    Exibe a lista de todos os produtos com seu saldo de estoque atual.
    """
    products = Product.objects.all().annotate(
        stock_balance=Sum('stockmovement__quantity', filter=Q(stockmovement__movement_type='IN')) -
                      Sum('stockmovement__quantity', filter=Q(stockmovement__movement_type='OUT'))
    )

    context = {
        'products': products
    }
    
    return render(request, 'stock/current_stock_list.html', context)


# --- Views para Movimentações de Estoque (CBVs) ---

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    """
    View para registrar uma compra (movimentação de entrada) de produto.
    """
    model = StockMovement
    form_class = PurchaseForm
    template_name = 'stock/stock_movement_form.html'
    success_url = reverse_lazy('stock:current_stock_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Registrar Compra (Entrada)'
        return context

    def form_valid(self, form):
        form.instance.movement_type = 'IN'
        form.instance.company = self.request.user.company
        form.instance.user = self.request.user
        
        response = super().form_valid(form)
        
        product = form.instance.product
        product.stock_quantity += form.instance.quantity
        product.save()

        messages.success(self.request, "Compra registrada e estoque atualizado!")
        return response

class SaleCreateView(LoginRequiredMixin, CreateView):
    """
    View para registrar uma venda (movimentação de saída) de produto.
    """
    model = StockMovement
    form_class = SaleForm
    template_name = 'stock/stock_movement_form.html'
    success_url = reverse_lazy('stock:current_stock_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Registrar Venda (Saída)'
        return context

    def form_valid(self, form):
        form.instance.movement_type = 'OUT'
        form.instance.company = self.request.user.company
        form.instance.user = self.request.user

        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']
        
        if quantity > product.stock_quantity:
            form.add_error('quantity', 'Quantidade insuficiente em estoque.')
            messages.error(self.request, "A quantidade de saída é maior que o estoque atual!")
            return self.form_invalid(form)

        response = super().form_valid(form)

        product.stock_quantity -= form.instance.quantity
        product.save()

        messages.success(self.request, "Venda registrada e estoque atualizado!")
        return response


# --- View para consulta de estoque em data específica (FBC) ---

def stock_at_date(request, product_id, year, month, day):
    """
    Calcula o saldo de estoque de um produto em uma data específica.
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Crie um objeto datetime para a data final do dia especificado
    end_of_day = datetime(year, month, day, 23, 59, 59)
    
    # Filtra os movimentos de estoque que ocorreram até a data final
    historical_movements = StockMovement.objects.filter(
        product=product,
        timestamp__lte=end_of_day
    )
    
    # Agrega a quantidade de entradas e saídas
    historical_stock = historical_movements.aggregate(
        in_qty=Sum('quantity', filter=Q(movement_type='IN')),
        out_qty=Sum('quantity', filter=Q(movement_type='OUT'))
    )
    
    in_qty = historical_stock['in_qty'] or 0
    out_qty = historical_stock['out_qty'] or 0
    
    stock_balance = in_qty - out_qty
    
    context = {
        'product': product,
        'stock_balance': stock_balance,
        'target_date': end_of_day.date(),
    }
    
    return render(request, 'stock/stock_at_date_detail.html', context)
