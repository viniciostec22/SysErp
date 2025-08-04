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
