from django.forms import ModelForm
from .models import Despesa, Conta
from django.forms import widgets


class DespesaForm(ModelForm):
    class Meta:
        model = Despesa
        fields = ['nome',
            'valor',
            'categoria',
            'dia_vencimento',
            'inicio',
            'termino',
            'cor',
            'icone',
            'periodica',
            'meses_periodo',
            'repeticao_anual',
            'observacao']
        #labels = { 'nome':'teste'}
        # error_messages = {
        #     'meses_periodo': {
        #         'max_value': 'A quantidade de mêses não pode ser maior que %(limit_value)s',
        #         'min_value': 'A quantidade de mêses não pode ser menor que %(limit_value)s',
        #     },
        # }
        # widgets = {
        #     'nome': widgets.TextInput(attrs={'class': 'input'}),
        #     'valor': widgets.NumberInput(attrs={'class': 'input'}),
        #     'dia_vencimento': widgets.Select(attrs={'class': 'select'}),
        #
        # }


class ContaForm(ModelForm):
    class Meta:
        model = Conta
        fields = ['despesa',
                    'valor',
                    'dia_vencimento',
                    'referente',
                    'observacao']