from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import datetime

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
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def criar_contas(self, data_referencia):
        MES_ATUAL = 1
        vencimento_atual = data_referencia.replace(day=self.dia_vencimento)
        meses_conta = range(self.mes_inicio, self.mes_termino + MES_ATUAL)
        data_ultima_conta_ano = vencimento_atual.replace(month=meses_conta[-1])
        ano_referencia = vencimento_atual.year
        contas = []
        if vencimento_atual > data_ultima_conta_ano:
            ano_referencia = +1
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

    def pagar(self):
        self.paga = True
        if self.data_alteracao_pagamento is None and self.despesa.repeticao_anual:
           nova_conta = self.despesa.criar_conta(datetime.date(self.referente.year + 1, self.referente.month, self.referente.day))
           nova_conta.save()
        self.data_alteracao_pagamento = timezone.now()
        self.save()

    def __str__(self):
        return 'Referencia :' + self.referente.strftime('%d/%m/%Y')
