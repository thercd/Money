from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import datetime

dias_vemcimento = [(i, i) for i in range(1, 31)]


class Despesa(models.Model):
    nome = models.CharField(max_length=40)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    dia_vencimento = models.PositiveIntegerField(choices=dias_vemcimento)
    mes_inicio = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(11)])
    mes_termino = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    cor = models.CharField(max_length=10, blank=True)
    icone = models.CharField(max_length=15, blank=True)
    categoria = models.CharField(max_length=21, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    periodica = models.BooleanField(default=False)
    repeticao_anual = models.BooleanField(default=False)
    observacao = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def criar_contas(self, data_referencia):
        MES_ATUAL = 1
        meses_conta = range(self.mes_inicio, self.mes_termino + MES_ATUAL)
        data_ultima_conta_ano = data_referencia.replace(month=meses_conta[-1], day=self.dia_vencimento)
        ano_referencia = data_referencia.year
        contas = []
        if data_referencia > data_ultima_conta_ano:
            ano_referencia += 1
        for mes in meses_conta:
            conta = self.criar_conta(datetime.date(ano_referencia, mes, self.dia_vencimento))
            contas.append(conta)
        return contas

    def criar_conta(self, data_referencia):
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
    data_alteracao_pagamento = models.DateTimeField(null=True, blank=True)
    observacao = models.TextField(blank=True)


    def __str__(self):
        return 'Referencia :' + self.referente.strftime('%d/%m/%Y')
