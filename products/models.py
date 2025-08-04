import uuid  # Importamos o módulo uuid
from django.db import models
from core.models import Company  # Importamos o modelo Company

class Brand(models.Model):
    """
    Representa uma marca de produto.
    Relacionada a uma empresa específica para o multitenancy.
    """
    # Usamos UUIDField como chave primária
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='brands')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

    class Meta:
        unique_together = ('company', 'name')
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

class Category(models.Model):
    """
    Representa uma categoria de produto.
    Também relacionada a uma empresa para o multitenancy.
    """
    # Usamos UUIDField como chave primária
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"
    
    class Meta:
        unique_together = ('company', 'name')
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Product(models.Model):
    """
    Representa um produto.
    Relacionado a Company, Brand e Category.
    """
    # Usamos UUIDField como chave primária
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # As ForeignKeys para Brand e Category também usarão UUIDs automaticamente
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    ncm = models.CharField(max_length=8, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'