from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms.models import model_to_dict
from django.forms import modelformset_factory
from .forms import DespesaForm, ContaForm
from .models import Despesa, Conta
import datetime


def index(request):
    return render(request, 'index.html')

def cadastro_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=True)
            return redirect(reverse('cadastro_conta', args=[despesa.id]))
    else:
        form = DespesaForm()
    return render(request, 'cadastro_despesa.html', {'form': form})


def cadastro_conta(request,despesa_id):
    contas = Conta.objects.filter(despesa=despesa_id)
    despesa = Despesa.objects.get(id=despesa_id)
    if contas:
        return HttpResponse('A despesa já possui as contas cadastradas')
    else:
        ContaFormSet = modelformset_factory(Conta, form=ContaForm, extra=12)
        if request.method == 'POST':
            formset = ContaFormSet(request.POST)
            if formset.is_valid():
                for contaForm in formset:
                    conta = contaForm.save(commit=False)
                    conta.despesa = despesa
                    conta.save()
                redirect(reverse('contas_cadastradas_sucesso', args=[despesa.id]))
            else:
                return render(request, 'parametrizar_contas.html', {'contas': formset, 'despesa_id': despesa_id})
        else:
            contas = despesa.criar_contas()
            contas_json = []
            for conta in contas:
                contas_json.append(model_to_dict(conta))
            formset = ContaFormSet(initial=contas_json, queryset=Conta.objects.none())
            return render(request, 'parametrizar_contas.html', {'contas': formset,'despesa_id': despesa_id})


def contas_cadastradas_sucesso(request, despesa_id):
    contas = Conta.objects.filter(despesa=despesa_id)
    return render(request, 'contas_cadastradas_sucesso.html', {'contas': contas})


def alteracao_despesa(request, despesa_id):
    despesa = Despesa.objects.get(id=despesa_id)
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.has_changed():
            if form.is_valid():
                despesa.save()
                return redirect(reverse('alteracao_contas', args=[despesa.id]))
            else:
                return HttpResponse('formulario invalido')
        else:
            return HttpResponse('nada mudou')
    else:
        form = DespesaForm(model_to_dict(despesa))
        return render(request, 'alteracao_despesa.html', {'form': form})


def alteracao_contas(request, despesa_id):
    despesa = Despesa.objects.get(id=despesa_id)
    data_vencimento_mes_atual = datetime.date.today().replace(day=despesa.dia_vencimento)
    if request.method == 'POST':
        ContaFormSet = modelformset_factory(Conta, form=ContaForm)
        formset = ContaFormSet(request.POST)
        if formset.is_valid():
            Conta.objects.filter(despesa=despesa.id, paga=False, referente__gte=data_vencimento_mes_atual).delete()
            for contaForm in formset:
                conta = contaForm.save(commit=False)
                conta.despesa = despesa
                conta.save()
            return redirect(reverse('contas_cadastradas_sucesso', args=[despesa.id]))
        else:
            return render(request, 'alterar_parametrizacao_contas.html', {'contas': formset, 'despesa_id': despesa_id})
        pass
    else:
        contas = despesa.criar_contas()
        ContaFormSet = modelformset_factory(Conta, form=ContaForm, extra=len(contas))
        contas_json = []
        for conta in contas:
            if conta.referente < data_vencimento_mes_atual:
                conta.referente = conta.referente.replace(year=conta.referente.year + 1)
            contas_json.append(model_to_dict(conta))
        formset = ContaFormSet(initial=sorted(contas_json, key= lambda x: x['referente']), queryset=Conta.objects.none())
        return render(request, 'alterar_parametrizacao_contas.html', {'contas': formset, 'despesa_id': despesa_id})


def listar_contas(request):
    data_atual = datetime.date.today()
    proximo_mes = (datetime.date.today() + datetime.timedelta(1*365/12)).replace(day=1)
    contas = Conta.objects.filter(referente__month=data_atual.month, referente__year=data_atual.year)
    proximas_contas = Conta.objects.filter(paga= False, referente__gte=proximo_mes).order_by('referente')[:7]
    return render(request, 'lista_contas.html', {'contas': contas, 'proximas_contas':proximas_contas})


def listar_contas_depesa(request, despesa_id):
    contas = Conta.objects.filter(despesa=despesa_id).order_by('referente')
    return render(request, 'lista_contas_despesa.html', {'contas': contas, 'despesa':despesa_id})


def pagar_conta(request,despesa_id,conta_id):
    conta = Conta.objects.get(id=conta_id)
    conta.pagar()
    ultima_pagina = request.META.get('HTTP_REFERER', None)
    if ultima_pagina is not None:
        return HttpResponseRedirect(ultima_pagina)
    else:
        return redirect(reverse('index'))


