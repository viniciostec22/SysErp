# sales/forms.py

from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    """
    Formulário para o modelo Customer.
    """
    class Meta:
        model = Customer
        fields = ['name', 'cpf_cnpj', 'email', 'phone', 'address', 'city', 'state', 'zip_code']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-input'}),
        #     'cpf_cnpj': forms.TextInput(attrs={'class': 'form-input'}),
        #     # Adicione outros widgets conforme necessário para o estilo
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Opcional: Adicione classes CSS do Tailwind para os campos do formulário
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
