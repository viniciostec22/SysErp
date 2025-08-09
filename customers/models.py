# customers/models.py

from django.db import models
from django.urls import reverse
from core.models import Company

class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = (
        ('PJ', 'Pessoa Jurídica'),
        ('PF', 'Pessoa Física'),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='customers'
    )
    customer_type = models.CharField(
        max_length=2,
        choices=CUSTOMER_TYPE_CHOICES,
        default='PJ',
        verbose_name="Tipo de Cliente"
    )
    name = models.CharField(max_length=200, verbose_name="Nome / Razão Social")
    contact_person = models.CharField(max_length=100, blank=True, verbose_name="Pessoa de Contato")
    cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name="CNPJ")
    cpf = models.CharField(max_length=14, blank=True, null=True, verbose_name="CPF")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    address = models.CharField(max_length=255, blank=True, verbose_name="Endereço")
    city = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=50, blank=True, verbose_name="Estado")
    zip_code = models.CharField(max_length=20, blank=True, verbose_name="CEP")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('customers:customer_detail', kwargs={'pk': self.pk})
