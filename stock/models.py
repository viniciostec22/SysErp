# stock/models.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from products.models import Product
from suppliers.models import Supplier
from customers.models import Customer
from core.models import Company

class StockMovement(models.Model):
    """
    Registra toda e qualquer movimentação de estoque, seja entrada, saída ou ajuste.
    É o coração do controle de estoque e a base para o histórico.
    """
    class MovementType(models.TextChoices):
        PURCHASE = 'IN', 'Compra (Entrada)'
        SALE = 'OUT', 'Venda (Saída)'
        ADJUSTMENT_IN = 'ADJ_IN', 'Ajuste (Entrada)'
        ADJUSTMENT_OUT = 'ADJ_OUT', 'Ajuste (Saída)'
        RETURN_IN = 'RET_IN', 'Devolução (Entrada)'
        RETURN_OUT = 'RET_OUT', 'Devolução (Saída)'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='stock_movements', verbose_name="Empresa")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements', verbose_name="Produto")
    
    movement_type = models.CharField(max_length=10, choices=MovementType.choices, verbose_name="Tipo de Movimento")
    quantity = models.IntegerField("Quantidade") # Positivo para entradas, Negativo para saídas
    
    # Preço/Custo no momento do movimento
    unit_price = models.DecimalField("Preço/Custo Unitário", max_digits=10, decimal_places=2)

    # Relações com a origem/destino do movimento
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fornecedor")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente")
    
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data do Movimento")

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} de {self.product.name}: {self.quantity}"

    def save(self, *args, **kwargs):
        # Garante que a quantidade seja negativa para saídas e positiva para entradas
        # Esta lógica é melhor aqui do que no form, pois se aplica a qualquer criação de objeto.
        if self.movement_type in [self.MovementType.SALE, self.MovementType.ADJUSTMENT_OUT, self.MovementType.RETURN_OUT]:
            if self.quantity > 0:
                self.quantity = -self.quantity
        else: # Entradas
            if self.quantity < 0:
                self.quantity = abs(self.quantity)

        # Antes de salvar, valida se há estoque suficiente para uma saída
        if self.pk is None and self.quantity < 0: # Apenas na criação de um novo movimento de saída
            stock_atual = self.product.stock_quantity
            if stock_atual < abs(self.quantity):
                raise ValidationError(
                    f"Estoque insuficiente para {self.product.name}. "
                    f"Disponível: {stock_atual}, Saída: {abs(self.quantity)}"
                )

        super().save(*args, **kwargs)

        # Após salvar, podemos recalcular o custo médio do produto (lógica a ser implementada)
        # Ex: self.product.recalculate_average_cost()
