# stock/forms.py
from django import forms
from .models import StockMovement
from products.models import Product
from suppliers.models import Supplier
from customers.models import Customer

class PurchaseForm(forms.ModelForm):
    """
    Formulário para registrar uma movimentação de COMPRA (Entrada).
    """
    class Meta:
        model = StockMovement
        fields = ['product', 'quantity', 'supplier', 'unit_price']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.company:
            # Filtra os produtos e fornecedores da empresa do usuário
            self.fields['product'].queryset = Product.objects.filter(company=user.company)
            self.fields['supplier'].queryset = Supplier.objects.filter(company=user.company)


class SaleForm(forms.ModelForm):
    """
    Formulário para registrar uma movimentação de VENDA (Saída).
    """
    class Meta:
        model = StockMovement
        fields = ['product', 'quantity', 'customer', 'unit_price']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.company:
            # Filtra os produtos e clientes da empresa do usuário
            self.fields['product'].queryset = Product.objects.filter(company=user.company)
            self.fields['customer'].queryset = Customer.objects.filter(company=user.company)

    def clean_quantity(self):
        # Valida se a quantidade não é negativa
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return quantity
