from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms.models import model_to_dict
from django.forms import modelformset_factory
from .forms import DespesaForm, ContaForm
from .models import Despesa, Conta
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


@login_required
def cadastro_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user
            despesa.save()
            return redirect(reverse('cadastro_conta', args=[despesa.id]))
    else:
        form = DespesaForm()
    return render(request, 'cadastro_despesa.html', {'form': form})


@login_required
def cadastro_conta(request,despesa_id):
    try:
        despesa = Despesa.objects.get(id=despesa_id, usuario=request.user)
        contas = Conta.objects.filter(despesa=despesa_id)
        if contas:
            return HttpResponse('A despesa já possui as contas cadastradas')
        else:
            ContaFormSet = modelformset_factory(Conta, form=ContaForm, max_num=12, can_delete=True)
            if request.method == 'POST':
                formset = ContaFormSet(request.POST)
                if formset.is_valid():
                    for contaForm in formset:
                        conta = contaForm.save(commit=False)
                        conta.despesa = despesa
                        conta.save()
                    return redirect(reverse('contas_cadastradas_sucesso', args=[despesa.id]))
                else:
                    return render(request, 'parametrizar_contas.html', {'contas': formset, 'despesa_id': despesa_id})
            else:
                contas = despesa.criar_contas(datetime.date.today())
                contas_json = []
                for conta in contas:
                    contas_json.append(model_to_dict(conta))
                formset = ContaFormSet(initial=contas_json, queryset=Conta.objects.none())
                formset.extra = len(contas)
                return render(request, 'parametrizar_contas.html', {'contas': formset,'despesa_id': despesa_id})
    except Despesa.DoesNotExist:
        return HttpResponse('Operaçao nao disponivel')


@login_required
def contas_cadastradas_sucesso(request, despesa_id):
    contas = Conta.objects.filter(despesa=despesa_id, despesa__usuario=request.user)
    if contas:
        return render(request, 'contas_cadastradas_sucesso.html', {'contas': contas})
    else:
        return HttpResponse('Operaçao nao disponivel')


@login_required
def alteracao_despesa(request, despesa_id):
    try:
        despesa = Despesa.objects.get(id=despesa_id, usuario=request.user)
        if request.method == 'POST':
            form = DespesaForm(request.POST, instance=despesa)
            if form.has_changed():
                if form.is_valid():
                    despesa.save()
                    return redirect(reverse('cadastro_conta', args=[despesa.id]))
                else:
                    return HttpResponse('formulario invalido')
            else:
                return HttpResponse('nada mudou')
        else:
            form = DespesaForm(model_to_dict(despesa))
            return render(request, 'alteracao_despesa.html', {'form': form})
    except Despesa.DoesNotExist:
        return HttpResponse('Operaçao nao disponivel')


@login_required
def listar_contas(request):
    data_atual = datetime.date.today()
    proximo_mes = (datetime.date.today() + datetime.timedelta(1*365/12)).replace(day=1)
    contas = Conta.objects.filter(despesa__usuario=request.user, referente__month=data_atual.month, referente__year=data_atual.year)
    proximas_contas = Conta.objects.filter(despesa__usuario=request.user, paga= False, referente__gte=proximo_mes).order_by('referente')[:7]
    return render(request, 'lista_contas.html', {'contas': contas, 'proximas_contas':proximas_contas})


@login_required
def listar_contas_depesa(request, despesa_id):
    contas = Conta.objects.filter(despesa=despesa_id, despesa__usuario=request.user).order_by('referente')
    return render(request, 'lista_contas_despesa.html', {'contas': contas, 'despesa':despesa_id})


@login_required
def pagar_conta(request, despesa_id, conta_id):
    try:
        despesa = Despesa.objects.get(id=despesa_id, usuario=request.user)
        conta = Conta.objects.get(id=conta_id, despesa__id=despesa_id)
        conta.paga = not conta.paga
        if conta.data_alteracao_pagamento is None and despesa.repeticao_anual:
            nova_conta = despesa.criar_conta(
                datetime.date(conta.referente.year + 1, conta.referente.month, conta.referente.day))
            nova_conta.save()
        conta.data_alteracao_pagamento = timezone.now()
        conta.save()
        ultima_pagina = request.META.get('HTTP_REFERER', None)
        if ultima_pagina is not None:
            return HttpResponseRedirect(ultima_pagina)
        else:
            return redirect(reverse('index'))
    except Despesa.DoesNotExist:
        return HttpResponse('Operaçao nao disponivel')
    except Conta.DoesNotExist:
        return HttpResponse('Operaçao nao disponivel')

