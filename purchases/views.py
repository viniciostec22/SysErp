# purchases/views.py

from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from .models import PurchaseInvoice, Supplier, Product # Importe os modelos aqui, para as novas APIs

from .forms import PurchaseInvoiceForm, InvoiceItemFormSet, PayableAccountFormSet


class PurchaseInvoiceCreateView(LoginRequiredMixin, View):
    template_name = 'purchases/purchase_invoice_form.html'

    def get(self, request, *args, **kwargs):
        """
        Lida com a requisição GET: mostra o formulário principal e os formsets em branco.
        """
        # Acessa a empresa do usuário logado
        user_company = request.user.company if hasattr(request.user, 'company') else None

        form = PurchaseInvoiceForm(user=request.user)
        # Passa a empresa para o formset para que ele possa filtrar os produtos
        item_formset = InvoiceItemFormSet(prefix='items', form_kwargs={'company': user_company})
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
        user_company = request.user.company if hasattr(request.user, 'company') else None
        form = PurchaseInvoiceForm(request.POST, user=request.user)
        item_formset = InvoiceItemFormSet(request.POST, prefix='items', form_kwargs={'company': user_company})
        payable_formset = PayableAccountFormSet(request.POST, prefix='payables')

        if form.is_valid() and item_formset.is_valid() and payable_formset.is_valid():
            try:
                with transaction.atomic():
                    company = request.user.company
                    if not company:
                        form.add_error(None, "Usuário não associado a uma empresa ativa.")
                        raise ValueError("Empresa não encontrada para o usuário.")

                    invoice = form.save(commit=False)
                    invoice.company = company
                    invoice.save()
                    
                    item_formset.instance = invoice
                    item_formset.save()
                    
                    payable_formset.instance = invoice
                    payable_formset.save()

                return redirect(reverse_lazy('purchases:purchase_list'))

            except Exception as e:
                context = {
                    'form': form,
                    'item_formset': item_formset,
                    'payable_formset': payable_formset,
                    'error_message': f"Ocorreu um erro ao salvar a nota: {e}"
                }
                return render(request, self.template_name, context)

        context = {
            'form': form,
            'item_formset': item_formset,
            'payable_formset': payable_formset,
        }
        return render(request, self.template_name, context)

class PurchaseInvoiceListView(LoginRequiredMixin, ListView):
    model = PurchaseInvoice
    template_name = 'purchases/purchase_invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'company') and user.company:
            return PurchaseInvoice.objects.filter(company=user.company).order_by('-issue_date')
        return PurchaseInvoice.objects.none()

# APIs para o Select2 (endpoints de busca)
# APIs para o Select2 (endpoints de busca)
def buscar_fornecedores(request):
    query = request.GET.get('q', '')
    empresa = request.user.company
    fornecedores = Supplier.objects.filter(company=empresa, name__icontains=query)
    # AQUI: Adicionamos mais campos ao resultado
    resultados = [{'id': f.pk, 'text': f.name, 'cnpj': f.cnpj, 'phone': f.phone, 'email': f.email} for f in fornecedores]
    return JsonResponse({'results': resultados})

def buscar_produtos(request):
    query = request.GET.get('q', '')
    empresa = request.user.company
    produtos = Product.objects.filter(company=empresa, name__icontains=query)
    resultados = [{'id': p.pk, 'text': p.name} for p in produtos]
    return JsonResponse({'results': resultados})
