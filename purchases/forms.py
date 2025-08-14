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
            'supplier': forms.Select(attrs={'class': 'select2-field w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'invoice_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Número da Nota Fiscal'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and hasattr(user, 'company') and user.company:
            self.fields['supplier'].queryset = Supplier.objects.filter(company=user.company)

class PurchaseInvoiceItemForm(forms.ModelForm):
    """
    Formulário para os itens da nota.
    """
    class Meta:
        model = PurchaseInvoiceItem
        fields = ('product', 'quantity', 'unit_cost')
        widgets = {
            'product': forms.Select(attrs={'class': 'select2-field w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'quantity': forms.NumberInput(attrs={'class': 'quantity-item w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Quantidade'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'unit-cost-item w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Custo Unitário'}),
        }
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

        if company:
            self.fields['product'].queryset = Product.objects.filter(company=company)

InvoiceItemFormSet = inlineformset_factory(
    PurchaseInvoice,
    PurchaseInvoiceItem,
    form=PurchaseInvoiceItemForm,
    fields=('product', 'quantity', 'unit_cost'),
    extra=0, 
    can_delete=True,
)

# AQUI: Novo formulário personalizado para o PayableAccountFormSet
class PayableAccountForm(forms.ModelForm):
    """
    Formulário para as parcelas, garantindo classes CSS para o JavaScript.
    """
    class Meta:
        model = PayableAccount
        fields=('due_date', 'amount')
        widgets={
            'due_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'amount': forms.NumberInput(
                attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white payable-amount-item', 'placeholder': 'Valor da Parcela', 'step': '0.01'}),
        }

# --- Formset para as PARCELAS (Contas a Pagar) ---
PayableAccountFormSet = inlineformset_factory(
    PurchaseInvoice, 
    PayableAccount, 
    form=PayableAccountForm, # Usa o novo formulário personalizado
    fields=('due_date', 'amount'),
    extra=1, 
    can_delete=True,
)
