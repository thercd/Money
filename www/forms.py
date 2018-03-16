from django.forms import ModelForm
from .models import Despesa, Conta
from django.forms import widgets
from django.core.validators import EMPTY_VALUES

import datetime
import re
from six import string_types

from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe


__all__ = ('MonthYearWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')


class MonthYearWidget(Widget):
    """
    A Widget that splits date input into two <select> boxes for month and year,
    with 'day' defaulting to the first of the month.

    Based on SelectDateWidget, in

    django/trunk/django/forms/extras/widgets.py


    """
    none_value = (0, '---')
    month_field = '%s_month'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)

    def render(self, name, value, attrs):
        try:
            year_val, month_val = value.year, value.month
        except AttributeError:
            year_val = month_val = None
            if isinstance(value, string_types):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        month_choices = list(MONTHS.items())
        if not (self.required and value):
            month_choices.append(self.none_value)
        month_choices.sort()
        local_attrs = self.build_attrs(base_attrs=attrs)
        s = Select(choices=month_choices)
        select_html = s.render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, self.none_value)
        local_attrs['id'] = self.year_field % id_
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == "0":
            return None
        if y and m:
            return '%s-%s-%s' % (y, m, 1)
        return data.get(name, None)

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

        widgets = {
            'referente': MonthYearWidget(),
            'data_pagamento': widgets.SelectDateWidget(),
        }

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

