# purchases/models.py

import uuid
from django.db import models
from django.conf import settings
from core.models import Company
from suppliers.models import Supplier
from products.models import Product
# O modelo StockMovement está em 'stock.models', vamos importá-lo na função
# para evitar importação circular, se necessário.

# --- 1. O Cabeçalho da Nota Fiscal de Compra ---
class PurchaseInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """
    Representa o cabeçalho de uma nota fiscal de compra.
    É o documento que agrupa os itens comprados e as condições de pagamento.
    """
    class InvoiceStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Rascunho'
        FINALIZED = 'FINALIZED', 'Finalizada'
        CANCELED = 'CANCELED', 'Cancelada'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='purchase_invoices', verbose_name="Empresa")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="Fornecedor")
    
    invoice_number = models.CharField(max_length=50, verbose_name="Número da Nota")
    issue_date = models.DateField(verbose_name="Data de Emissão")
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor Total da Nota")
    status = models.CharField(max_length=10, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT, verbose_name="Status")
    
    created_at = models.DateTimeField(auto_now_add=True)
    finalized_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de Finalização")
    
    class Meta:
        verbose_name = "Nota de Compra"
        verbose_name_plural = "Notas de Compra"
        unique_together = ('company', 'supplier', 'invoice_number')

    def __str__(self):
        return f"Nota {self.invoice_number} - {self.supplier.name}"

# --- 2. Os Itens da Nota Fiscal ---
class PurchaseInvoiceItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """
    Representa cada linha de produto dentro de uma Nota de Compra.
    """
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items', verbose_name="Nota de Compra")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produto")
    quantity = models.PositiveIntegerField(verbose_name="Quantidade")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Custo Unitário")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Custo Total do Item")

    def save(self, *args, **kwargs):
        # Calcula o custo total do item automaticamente
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} na Nota {self.invoice.invoice_number}"

# --- 3. As Contas a Pagar (Duplicatas/Parcelas) ---
class PayableAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """
    Representa uma conta a pagar, geralmente uma parcela de uma nota de compra.
    """
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pendente'
        PAID = 'PAID', 'Paga'
        OVERDUE = 'OVERDUE', 'Vencida'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payables', verbose_name="Empresa")
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='installments', verbose_name="Nota de Origem")
    
    due_date = models.DateField(verbose_name="Data de Vencimento")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor da Parcela")
    
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, verbose_name="Status")
    payment_date = models.DateField(null=True, blank=True, verbose_name="Data de Pagamento")

    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"
        ordering = ['due_date']

    def __str__(self):
        return f"Parcela de {self.amount} da Nota {self.invoice.invoice_number} (Vence: {self.due_date})"
