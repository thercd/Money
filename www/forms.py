from django.forms import ModelForm
from .models import Despesa, Conta
from django.forms import widgets
from django.core.validators import EMPTY_VALUES


class DespesaForm(ModelForm):
    class Meta:
        JANEIRO_NOVEMBRO = (
            ('', 'Mes'),
            ('1', 'Janeiro'),
            ('2', 'Fevereiro'),
            ('3', 'Março'),
            ('4', 'Abril'),
            ('5', 'Maio'),
            ('6', 'Junho'),
            ('7', 'Julho'),
            ('8', 'Agosto'),
            ('9', 'Setembro'),
            ('10', 'Outubro'),
            ('11', 'Novembro'),
        )

        FEVEREIRO_DEZEMBRO = (
            ('', 'Mes'),
            ('2', 'Fevereiro'),
            ('3', 'Março'),
            ('4', 'Abril'),
            ('5', 'Maio'),
            ('6', 'Junho'),
            ('7', 'Julho'),
            ('8', 'Agosto'),
            ('9', 'Setembro'),
            ('10', 'Outubro'),
            ('11', 'Novembro'),
            ('12', 'Dezembro'),
        )
        model = Despesa
        fields = ['nome',
            'estimativa',
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
        widgets = {
            # 'nome': widgets.TextInput(attrs={'class': 'input'}),
            # 'valor': widgets.NumberInput(attrs={'class': 'input'}),
            'mes_inicio': widgets.Select(choices=JANEIRO_NOVEMBRO),
            'mes_termino': widgets.Select(choices=FEVEREIRO_DEZEMBRO),
        }

    def clean(self):
        periodica = self.cleaned_data.get('periodica', False)
        if periodica:
            mes_inicio = self.cleaned_data.get('mes_inicio', None)
            mes_termino = self.cleaned_data.get('mes_termino', None)
            if mes_inicio in EMPTY_VALUES:
                self._errors['mes_inicio'] = self.error_class([
                    'O Mes de inicio é necessario quando a divida é periodica'])
            if mes_termino in EMPTY_VALUES:
                self._errors['mes_termino'] = self.error_class([
                    'O Mes de termino é necessario quando a divida é periodica'])
            if mes_inicio and mes_termino and mes_inicio > mes_termino:
                self._errors['mes_inicio'] = self.error_class([
                    'O Mes de inicio deve ser menor que o termino'])
                self._errors['mes_termino'] = self.error_class([
                    'O Mes de termino deve ser maior que o inicio'])
        else:
            del self.cleaned_data['mes_inicio']
            del self.cleaned_data['mes_termino']
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
        labels = {'dia_vencimento': 'Vencimento'}

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

