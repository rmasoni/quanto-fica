from decimal import ROUND_HALF_UP, Decimal

from django import forms

from .models import Currency


class NubankExchangeRateForm(forms.Form):

    currency = forms.ModelChoiceField(
        queryset = Currency.objects.all(),
        empty_label = None,
        required = True,
        widget = forms.Select(
            attrs = {
                'id': 'input__unit',
                'class': 'input__unit'
            },
        )
    )

    value = forms.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        required = True
    )

    def calculate(self):
        currency = self.cleaned_data.get('currency')
        purchase_value = self.cleaned_data.get('value')
        exchange_rate = currency.current_rate.value
        spread = Decimal('0.04')
        nubank_exchange_rate = exchange_rate + (exchange_rate * spread)
        brl_purchase_value = purchase_value * nubank_exchange_rate
        iof_rate = Decimal('0.0638')
        iof = brl_purchase_value * iof_rate
        total = brl_purchase_value + iof
        data = {
            "ptax_exchange_rate": exchange_rate,
            "spread": spread,
            "nubank_exchange_rate": nubank_exchange_rate,
            "subtotal": brl_purchase_value.quantize(Decimal('0.01'), ROUND_HALF_UP),
            "iof_rate": iof_rate,
            "iof": iof.quantize(Decimal('0.01'), ROUND_HALF_UP),
            "total": total.quantize(Decimal('0.01'), ROUND_HALF_UP)
        }
        return data
