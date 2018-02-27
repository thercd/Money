from django.forms import ModelForm
from .models import Despesa
from django.forms import widgets


class DespesaForm(ModelForm):
    class Meta:
        model = Despesa
        fields = ['nome',
            'valor',
            'dia_vencimento',
            'inicio',
            'termino',
            'tipo',
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