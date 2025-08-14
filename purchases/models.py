# purchases/models.py
from django.db import models
from core.models import Company
from suppliers.models import Supplier
from products.models import Product

class PurchaseInvoice(models.Model):
    class InvoiceStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Rascunho'
        FINALIZED = 'FINALIZED', 'Finalizada'
        CANCELED = 'CANCELED', 'Cancelada'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='purchase_invoices')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    invoice_number = models.CharField(max_length=50)
    issue_date = models.DateField()
    
    # NOVOS CAMPOS DE RESUMO
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    freight = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    other_costs = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=10, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    finalized_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Nota de Compra"
        verbose_name_plural = "Notas de Compra"
        unique_together = ('company', 'supplier', 'invoice_number')

    def __str__(self):
        return f"Nota {self.invoice_number} - {self.supplier.name}"

class PurchaseInvoiceItem(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2) # Alterado para Decimal
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

class PayableAccount(models.Model):
    # ... (mantenha este modelo como está)
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pendente'
        PAID = 'PAID', 'Paga'
        OVERDUE = 'OVERDUE', 'Vencida'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payables')
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='installments')
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"
        ordering = ['due_date']