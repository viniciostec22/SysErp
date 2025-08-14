# purchases/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseInvoice, PurchaseInvoiceItem, PayableAccount
from suppliers.models import Supplier
from products.models import Product

class PurchaseInvoiceForm(forms.ModelForm):
    """
    Formulário para o cabeçalho da Nota de Compra.
    """
    class Meta:
        model = PurchaseInvoice
        fields = ['supplier', 'invoice_number', 'issue_date']
        widgets = {
            'issue_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}
            ),
            'supplier': forms.Select(attrs={'class': 'autocomplete, w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white select2-field'}),
            'invoice_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Número da Nota   Fiscal  '}),
        }

    def __init__(self, *args, **kwargs):
        # Captura o usuário da view para filtrar os fornecedores
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and hasattr(user, 'company') and user.company:
            self.fields['supplier'].queryset = Supplier.objects.filter(company=user.company)

# --- Formset para os ITENS da Nota ---
# O formset permite adicionar vários produtos na mesma nota de forma dinâmica
InvoiceItemFormSet = inlineformset_factory(
    PurchaseInvoice,  # Modelo Pai
    PurchaseInvoiceItem,  # Modelo Filho
    fields=('product', 'quantity', 'unit_cost'),
    extra=1,  # Começa com 1 formulário de item em branco
    can_delete=True,  # Permite remover itens
    widgets={
        'product': forms.Select(attrs={'class': 'select2-field product-item w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
        'quantity': forms.NumberInput(attrs={'class': 'quantity-item w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Quantidade'}),
        'unit_cost': forms.NumberInput(attrs={'class': 'unit-cost-item w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Custo Unitário'}),
    }
)

# --- Formset para as PARCELAS (Contas a Pagar) ---
PayableAccountFormSet = inlineformset_factory(
    PurchaseInvoice, # Modelo Pai
    PayableAccount, # Modelo Filho
    fields=('due_date', 'amount'),
    extra=1, # Começa com 1 formulário de parcela em branco
    can_delete=True, # Permite remover parcelas
    widgets={
        'due_date': forms.DateInput(
            attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}
        ),
        'amount': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Valor da Parcela'}),
    }
)
