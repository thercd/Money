from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

dias_vemcimento = [(i, i) for i in range(1, 31)]


class Despesa(models.Model):
    quantidade_meses_disponiveis = [(i, i) for i in range(1, 12)]
    nome = models.CharField(max_length=40)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    dia_vencimento = models.PositiveIntegerField(choices=dias_vemcimento)
    inicio = models.DateField(default=timezone.now)
    termino = models.DateField(blank=True, null=True)
    cor = models.CharField(max_length=10, blank=True)
    icone = models.CharField(max_length=15, blank=True)
    categoria = models.CharField(max_length=21, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    periodica = models.BooleanField(default=False)
    meses_periodo = models.PositiveIntegerField(choices=quantidade_meses_disponiveis, null=True)
    repeticao_anual = models.BooleanField(default=False)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class Conta(models.Model):
    despesa = models.ForeignKey(Despesa, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    dia_vencimento = models.PositiveIntegerField(choices=dias_vemcimento)
    data_criacao = models.DateTimeField(auto_now_add=True)
    referente = models.DateTimeField()
    paga = models.BooleanField(default=False)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return self.nome