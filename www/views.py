from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
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
            form.save(commit=True)
    else:
        form = DespesaForm()
    return render(request, 'cadastro_despesa.html', {'form': form})

def cadastro_conta(request,despesa_id):
    if request.method == 'POST':
        pass
    else:
        despesa = Despesa.objects.get(id=despesa_id)
        mes_atual = datetime.datetime.now().month


def hero(request):
    return render(request, 'hero.html')
