from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

dias_vemcimento = [(i, i) for i in range(1, 31)]


class Despesa(models.Model):
    nome = models.CharField(max_length=40)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    dia_vencimento = models.PositiveIntegerField(choices=dias_vemcimento)
    mes_inicio = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(12)])
    mes_termino = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(12)])
    cor = models.CharField(max_length=10, blank=True)
    icone = models.CharField(max_length=15, blank=True)
    categoria = models.CharField(max_length=21, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    periodica = models.BooleanField(default=False)
    repeticao_anual = models.BooleanField(default=False)
    observacao = models.TextField(blank=True)

    def criarConta(self, data_referencia):
        conta = Conta()
        conta.despesa = self
        conta.valor = self.valor
        conta.dia_vencimento = self.dia_vencimento
        conta.referente = data_referencia
        return conta

    def __str__(self):
        return self.nome


class Conta(models.Model):
    despesa = models.ForeignKey(Despesa, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    dia_vencimento = models.PositiveIntegerField(choices=dias_vemcimento)
    data_criacao = models.DateTimeField(auto_now_add=True)
    referente = models.DateField()
    paga = models.BooleanField(default=False)
    data_pagamento = models.DateField(null=True, blank=True)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return 'Referencia :' + self.referente.strftime('%d/%m/%Y')
