# purchases/views.py

from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from .models import Supplier, Product

from .models import PurchaseInvoice
from .forms import PurchaseInvoiceForm, InvoiceItemFormSet, PayableAccountFormSet


class PurchaseInvoiceCreateView(LoginRequiredMixin, View):
    template_name = 'purchases/purchase_invoice_form.html'

    def get(self, request, *args, **kwargs):
        """
        Lida com a requisição GET: mostra o formulário principal e os formsets em branco.
        """
        form = PurchaseInvoiceForm(user=request.user)
        item_formset = InvoiceItemFormSet(prefix='items')
        payable_formset = PayableAccountFormSet(prefix='payables')
        
        context = {
            'form': form,
            'item_formset': item_formset,
            'payable_formset': payable_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Lida com a requisição POST: processa e valida todos os formulários.
        """
        form = PurchaseInvoiceForm(request.POST, user=request.user)
        item_formset = InvoiceItemFormSet(request.POST, prefix='items')
        payable_formset = PayableAccountFormSet(request.POST, prefix='payables')

        if form.is_valid() and item_formset.is_valid() and payable_formset.is_valid():
            try:
                # Usa uma transação atômica para garantir a integridade dos dados.
                # Ou tudo é salvo, ou nada é.
                with transaction.atomic():
                    # Pega a empresa do usuário logado
                    company = request.user.company
                    if not company:
                        # Adiciona um erro se o usuário não tiver uma empresa ativa
                        form.add_error(None, "Usuário não associado a uma empresa ativa.")
                        raise ValueError("Empresa não encontrada para o usuário.")

                    # Salva o formulário principal (cabeçalho da nota)
                    invoice = form.save(commit=False)
                    invoice.company = company
                    invoice.save()

                    # Associa os itens e parcelas à nota recém-criada e salva
                    # O 'instance=invoice' faz a ligação entre o filho e o pai.
                    item_formset.instance = invoice
                    item_formset.save()
                    
                    payable_formset.instance = invoice
                    payable_formset.save()

                # Redireciona para uma página de sucesso (ex: lista de notas)
                return redirect(reverse_lazy('purchases:purchase_list')) # Crie esta URL depois

            except Exception as e:
                # Se ocorrer um erro, a transação é revertida.
                # Renderiza a página novamente com os formulários e a mensagem de erro.
                context = {
                    'form': form,
                    'item_formset': item_formset,
                    'payable_formset': payable_formset,
                    'error_message': f"Ocorreu um erro ao salvar a nota: {e}"
                }
                return render(request, self.template_name, context)

        # Se algum formulário for inválido, renderiza a página novamente com os erros
        context = {
            'form': form,
            'item_formset': item_formset,
            'payable_formset': payable_formset,
        }
        return render(request, self.template_name, context)

# --- View para listar as notas já criadas ---
class PurchaseInvoiceListView(LoginRequiredMixin, ListView):
    model = PurchaseInvoice
    template_name = 'purchases/purchase_invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        # Filtra as notas para mostrar apenas as da empresa do usuário logado
        user = self.request.user
        if hasattr(user, 'company') and user.company:
            return PurchaseInvoice.objects.filter(company=user.company).order_by('-issue_date')
        return PurchaseInvoice.objects.none()
