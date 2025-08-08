# stock/models.py

import uuid
from django.db import models
from core.models import Company, User # Importação corrigida para o seu modelo User
from products.models import Product

class StockMovement(models.Model):
    """
    Registra cada transação de estoque (entrada ou saída) para um produto.
    Este modelo garante o histórico imutável do estoque.
    """
    # Choices para o tipo de movimento
    MOVEMENT_TYPE_CHOICES = [
        ('IN', 'Entrada'),
        ('OUT', 'Saída'),
    ]

    # Usamos UUIDField como chave primária
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Relação com a empresa
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='stock_movements')
    # Relação com o produto
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    # Tipo de movimento (Entrada ou Saída)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    # Quantidade de itens movimentados, agora como IntegerField
    quantity = models.IntegerField()
    # Usuário que realizou a operação, referenciando seu modelo User personalizado
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_movements')
    # Motivo do movimento (compra, venda, ajuste, etc.)
    reason = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    # Data e hora da transação
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_movement_type_display()} de {self.quantity} para {self.product.name}"

    class Meta:
        verbose_name = 'Movimento de Estoque'
        verbose_name_plural = 'Movimentos de Estoque'
        ordering = ['-timestamp'] # Ordena por data e hora decrescente
