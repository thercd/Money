from django.forms import ModelForm
from .models import Despesa, Conta
from django.forms import widgets
from django.core.validators import EMPTY_VALUES


class DespesaForm(ModelForm):
    class Meta:
        model = Despesa
        fields = ['nome',
            'valor',
            'categoria',
            'dia_vencimento',
            'mes_inicio',
            'mes_termino',
            'cor',
            'icone',
            'periodica',
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

    def clean(self):
        periodica = self.cleaned_data.get('periodica', False)
        if periodica:
            mes_inicio = self.cleaned_data.get('mes_inicio', None)
            if mes_inicio in EMPTY_VALUES:
                self._errors['mes_inicio'] = self.error_class([
                    'O Mes de inicio é necessario quando a divida é periodica'])
            mes_termino = self.cleaned_data.get('mes_termino', None)
            if mes_termino in EMPTY_VALUES:
                self._errors['mes_termino'] = self.error_class([
                    'O Mes de termino é necessario quando a divida é periodica'])
        return self.cleaned_data


class ContaForm(ModelForm):
    class Meta:
        model = Conta
        fields = ['valor',
                'dia_vencimento',
                'referente',
                'paga',
                'data_pagamento',
                'observacao']
    def clean(self):
        paga = self.cleaned_data.get('paga', False)
        data_pagamento = self.cleaned_data.get('data_pagamento', None)
        if data_pagamento in EMPTY_VALUES and paga:
                self._errors['data_pagamento'] = self.error_class([
                    'Caso a divida estiver paga é necessario informar a data de pagamento '])
        elif data_pagamento not in EMPTY_VALUES and not paga:
            self._errors['data_pagamento'] = self.error_class([
                'A conta nao está marcada como paga'])
        return self.cleaned_data