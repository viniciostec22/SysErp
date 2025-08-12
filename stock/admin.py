# stock/admin.py
from django.contrib import admin
from .models import StockMovement

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    """
    Configuração do painel de administração para o modelo StockMovement.
    Garante que os campos exibidos em list_display correspondam aos campos do modelo.
    """
    list_display = (
        'product',
        'movement_type',
        'quantity',
        'user',
        'company'
    )
    list_filter = ('movement_type', 'company')
    search_fields = ('product__name', 'user__username', 'company__name')
    

