import uuid 
from django.db import models
from django.core.validators import MinLengthValidator
from core.models import Company # Assumindo que a classe Company está em users.models

class Supplier(models.Model):
    """
    Representa um fornecedor de produtos.
    Um fornecedor é associado a uma única empresa.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='suppliers')
    name = models.CharField(max_length=255, verbose_name="Nome do Fornecedor", help_text="O nome completo do fornecedor.")
    #contact_person = models.CharField(max_length=255, verbose_name="Pessoa de Contato", blank=True, null=True, help_text="O nome da pessoa de contato na empresa do fornecedor.")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ", validators=[MinLengthValidator(14)], help_text="Número de Cadastro Nacional da Pessoa Jurídica.")
    phone = models.CharField(max_length=20, verbose_name="Telefone", help_text="Número de telefone para contato.")
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Endereço de email para contato.")
    address = models.CharField(max_length=255, verbose_name="Endereço", help_text="Endereço completo do fornecedor.")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado", help_text="Sigla do estado (ex: SP, RJ).")
    zip_code = models.CharField(max_length=10, verbose_name="CEP", blank=True, null=True, help_text="Código de Endereçamento Postal.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado Em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado Em")
    active = models.BooleanField(default=True, verbose_name="Ativo", help_text="Indica se o fornecedor está ativo no sistema.")

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['name']

    def __str__(self):
        return self.name
