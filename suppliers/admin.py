from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'email', 'company', 'active')
    list_filter = ('company', 'active')
    search_fields = ('name', 'cnpj')