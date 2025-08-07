from django import forms
from . import models

class BrandForm(forms.ModelForm):
    class Meta:
        model = models.Brand
        # Removemos 'company' dos fields. Ele não será exibido no formulário.
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nome da Marca',
        }
    
    # O método __init__ não precisa mais manipular o campo 'company'
    # pois ele não estará mais nos fields do formulário.
    def __init__(self, *args, **kwargs):
        # O 'request' é passado para o form_class através da view (se necessário),
        # mas como o campo 'company' será injetado pela view,
        # não precisamos mais do 'request' aqui para filtrar o queryset do campo 'company'.
        # Se você precisar do 'request' para outras lógicas no formulário,
        # pode passá-lo como 'form_kwargs={'request': self.request}' na view
        # e recebê-lo aqui como 'self.request = kwargs.pop('request', None)'.
        super().__init__(*args, **kwargs)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        # Removemos 'company' dos fields. Ele não será exibido no formulário.
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nome da Categoria',
        }
    
    # O método __init__ não precisa mais manipular o campo 'company'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'category', 'brand', 'description', 'barcode', 'cost', 'price', 'sku', 'ncm']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Digite o título do produto'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white select2-field', 'placeholder': 'Selecionar categoria'}),
            'brand': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white select2-field', 'placeholder': 'Selecionar marca'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'rows': 3, 'placeholder': 'Descreva o produto detalhadamente...'}),
            'barcode': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Ex: 1234567890123'}),
            'sku': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'Ex: PROD-001'}),
            'cost': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'R$ 0,00'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white', 'placeholder': 'R$ 0,00'}),
        }
        labels = {
            'name': 'Produto',
            'category': 'Categoria',
            'brand': 'Marca',
            'description': 'Descrição',
            'barcode': 'Código de Barras',
            'sku': 'SKU',
            'ncm': 'NCM',
            'cost': 'Preço de Custo',
            'price': 'Preço de Venda',
        }

    # Adicionamos o método __init__ para filtrar as opções de Brand e Category
    def __init__(self, *args, **kwargs):
        # Capturamos o request da view antes de chamar o super().__init__()
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request and request.user.is_authenticated:
            company_user = request.user.company_links.filter(active=True).first()
            if company_user:
                # Filtramos as opções de Brand e Category para mostrar apenas as da empresa do usuário
                self.fields['category'].queryset = models.Category.objects.filter(company=company_user.company)
                self.fields['brand'].queryset = models.Brand.objects.filter(company=company_user.company)
