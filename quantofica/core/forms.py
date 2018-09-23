import decimal

from django import forms

from .models import Currency


class NubankExchangeRateForm(forms.Form):
    moeda = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        empty_label=None,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'input__unit'
            },

        )
    )
    valor = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Valor da compra',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'autofocus': 'autofocus',
                'class': 'input__field',
                'step': 'any'
            },
        )
    )

    def calculate(self):
        currency = self.cleaned_data.get('moeda')
        purchase_value = self.cleaned_data.get('valor')
        rate = currency.get_current_rate()
        total = round((purchase_value * rate.value) * decimal.Decimal(1.1038), 2)
        formatted_total = '{symbol} {total}'.format(symbol=currency.symbol, total=total)
        return formatted_total
