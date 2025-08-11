from django import forms
from django.core.exceptions import ValidationError
from .models import Supplier

class SupplierForm(forms.ModelForm):
    """
    Formulário para criar ou editar um fornecedor.
    Usa ModelForm para gerar campos com base no modelo Supplier.
    """
    class Meta:
        model = Supplier
        fields = [
            'name', 'cnpj', 'phone', 'email', 
            'address', 'city', 'state', 'zip_code', 'active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            #'contact_person': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'cnpj': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'state': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'zip_code': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'active': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-blue-600 shadow-sm dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:ring-blue-500'}),
        }
        
        labels = {
            'name': 'Razão Social',
            'contact_person': 'Pessoa de Contato',
            'cnpj': 'CNPJ',
            'phone': 'Telefone',
            'email': 'E-mail',
            'address': 'Endereço',
            'city': 'Cidade',
            'state': 'Estado',
            'zip_code': 'CEP',
            'active': 'Ativo'
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        # Remove a formatação do CNPJ para validação
        cnpj_cleaned = ''.join(filter(str.isdigit, cnpj))
        
        # O CNPJ deve ter 14 dígitos após a limpeza
        if len(cnpj_cleaned) != 14:
            raise ValidationError("O CNPJ deve conter 14 dígitos.")
        
        # Lógica de validação básica do CNPJ (pode ser mais completa se necessário)
        if cnpj_cleaned == cnpj_cleaned[0] * 14:
            raise ValidationError("CNPJ inválido.")
            
        return cnpj_cleaned

