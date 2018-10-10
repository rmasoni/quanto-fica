import decimal

from django import forms

from .models import Currency


class NubankExchangeRateForm(forms.Form):
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        empty_label=None,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'input__unit'
            },
        )
    )
    value = forms.DecimalField(
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
        currency = self.cleaned_data.get('currency')
        purchase_value = self.cleaned_data.get('value')
        total = round((purchase_value * currency.current_rate.value) * decimal.Decimal(1.1038), 2)
        return total
