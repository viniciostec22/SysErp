import uuid  # Importamos o módulo uuid
from django.db import models
from django.db.models import Sum
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
        return self.name

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
        return self.name
    
    class Meta:
        unique_together = ('company', 'name')
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

# --- Modelo Principal do Produto ---
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """
    Representa um produto no sistema. A quantidade em estoque não é armazenada
    diretamente aqui, mas calculada a partir dos movimentos de estoque.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products', verbose_name="Empresa")
    name = models.CharField(max_length=255, verbose_name="Nome do Produto")
    sku = models.CharField(max_length=100, blank=True, null=True, verbose_name="SKU (Código)")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    
    # Relações
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Marca")

    # Campos Financeiros
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço de Venda")
    average_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Custo Médio")
    
    active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        unique_together = ('company', 'sku') # SKU deve ser único por empresa
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku or 'Sem SKU'})"

    @property
    def stock_quantity(self):
        """
        Calcula a quantidade atual em estoque somando todos os movimentos.
        Esta é uma propriedade 'read-only'.
        """
        # O related_name 'movements' vem do ForeignKey no modelo StockMovement
        total = self.movements.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        return total if total is not None else 0