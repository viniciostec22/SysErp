from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

class CompanyFilteredMixin:
    """
    Mixin para filtrar o queryset de uma view para mostrar apenas
    os objetos associados à empresa do usuário logado.
    """
    def get_queryset(self):
        # Acede ao queryset base do modelo
        queryset = super().get_queryset()
        
        # Obtém a empresa do usuário logado usando a relação de muitos para muitos
        company_user = self.request.user.company_links.filter(active=True).first()
        
        # Filtra o queryset com base na empresa se existir
        if company_user:
            return queryset.filter(company=company_user.company)
            
        # Se o usuário não tiver uma empresa ativa, retorna um queryset vazio
        return self.model.objects.none()


class CompanyAssignMixin:
    """
    Mixin para atribuir automaticamente a empresa ativa do usuário
    ao objeto antes de salvar no CreateView.
    """
    def form_valid(self, form):
        company_user = self.request.user.company_links.filter(active=True).first()
        if company_user:
            form.instance.company = company_user.company
        else:
            messages.error(self.request, "Nenhuma empresa ativa associada a este usuário.")
            return redirect('home')
        return super().form_valid(form)
