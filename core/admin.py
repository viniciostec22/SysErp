# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company, CompanyUser

# Personaliza o painel de administração para o modelo User
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Campos que serão exibidos na lista de usuários no admin
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    # Campos que podem ser usados para buscar usuários
    search_fields = ('email',)
    # Campos que podem ser usados para filtrar a lista de usuários
    list_filter = ('is_staff', 'is_active')
    # Campos que não serão editáveis ao adicionar/editar um usuário
    readonly_fields = ('date_joined', 'last_login')

    # Define os fieldsets (grupos de campos) para a página de edição do usuário
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    # Remove o campo 'username' do formulário de criação/edição, já que usamos email
    filter_horizontal = ('groups', 'user_permissions',) # Mantém a interface de seleção de muitos para muitos

    # Sobrescreve o método para adicionar um novo usuário, garantindo que o username não seja obrigatório
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_new_user = obj is None
        if is_new_user:
            # Remove o campo username para criação de novo usuário
            if 'username' in form.base_fields:
                form.base_fields['username'].required = False
        return form


# Registra o modelo Company no painel de administração
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'city', 'state', 'created_at', 'updated_at')
    search_fields = ('name', 'cnpj')
    list_filter = ('state',)
    readonly_fields = ('created_at', 'updated_at')

# Registra o modelo CompanyUser no painel de administração
@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role', 'active', 'created_at')
    search_fields = ('user__email', 'company__name') # Permite buscar por email do usuário ou nome da empresa
    list_filter = ('role', 'active', 'company')
    readonly_fields = ('created_at', 'update_at')