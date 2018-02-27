from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import DespesaForm


def index(request):
    return render(request, 'index.html')


def cadastro_despesa(request):
    if request.method == 'POST':
        form = DespesaForm(data=request.POST)
        if form.is_valid():
            form.save(commit=True)
    else:
        form = DespesaForm()
    return render(request, 'cadastro_despesa.html', {'form': form})


def hero(request):
    return render(request, 'hero.html')
