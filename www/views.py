from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms.models import model_to_dict
from .forms import DespesaForm, ContaForm
from .models import Despesa, Conta
import datetime



def index(request):
    return render(request, 'index.html')


def cadastro_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        print(form.errors)
        if form.is_valid():
            despesa = form.save(commit=True)
            return redirect(reverse('cadastro_conta', args=[despesa.id]))
    else:
        form = DespesaForm()
    return render(request, 'cadastro_despesa.html', {'form': form})

def cadastro_conta(request,despesa_id):
    if request.method == 'POST':
        pass
    else:
        MES_ATUAL = 1
        despesa = Despesa.objects.get(id=despesa_id)
        vencimento_atual = datetime.date.today().replace(day=despesa.dia_vencimento)
        meses_conta = range(despesa.mes_inicio, despesa.mes_termino + MES_ATUAL)
        data_ultima_conta_ano = vencimento_atual.replace(month=meses_conta[-1])
        ano_referencia = vencimento_atual.year
        contas = []
        if vencimento_atual > data_ultima_conta_ano:
            ano_referencia=+1
            for mes in meses_conta:
                conta = despesa.criarConta(datetime.date(ano_referencia, mes, 1))
                conta.save()
                contas.append(ContaForm(model_to_dict(conta)))
        else:
            vencidas = 0
            for mes in meses_conta:
                conta = despesa.criarConta(datetime.date(ano_referencia, mes, despesa.dia_vencimento))
                if vencimento_atual > conta.referente:
                    vencidas += 1
                conta.save()
                contas.append(ContaForm(model_to_dict(conta)))

            if vencidas and despesa.repeticao_anual > 0:
                ano_referencia += 1
                for mes in meses_conta[0:vencidas]:
                    conta = despesa.criarConta(datetime.date(ano_referencia, mes, 1))
                    conta.save()
                    contas.append(ContaForm(model_to_dict(conta)))
        print(contas)
        return render(request, 'parametrizar_contas.html', {'contas':contas})

def listar_contas(request):
    data_atual = datetime.date.today()
    proximo_mes = (datetime.date.today() + datetime.timedelta(1*365/12)).replace(day=1)
    contas = Conta.objects.filter(referente__month=data_atual.month, referente__year=data_atual.year)
    proximas_contas = Conta.objects.filter(paga= False, referente__gte=proximo_mes ).order_by('referente')[:7]
    return render(request, 'lista_contas.html', {'contas': contas, 'proximas_contas':proximas_contas})

def listar_contas_depesa(request, despesa_id):
    contas = Conta.objects.filter(despesa=despesa_id)
    return render(request, 'lista_contas_despesa.html', {'contas': contas})





def hero(request):
    return render(request, 'hero.html')
