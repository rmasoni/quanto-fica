from django.shortcuts import render

from quantofica.core.forms import NubankExchangeRateForm
from quantofica.core.models import Currency


def get_default_currency():
    currency, created = Currency.objects.get_or_create(code='USD', defaults={
        'name': 'Dolar Americano',
        'symbol': 'US$',
        'central_bank_reference': 61
    })
    return currency

def home(request):
    output = None
    default_currency = get_default_currency()
    if 'moeda' in request.GET and 'valor' in request.GET:
        form = NubankExchangeRateForm(request.GET)
        if form.is_valid():
            output = form.calculate()
        default_currency = form.cleaned_data.get('moeda', default_currency)
    else:
        form = NubankExchangeRateForm(initial={'moeda': default_currency})
    return render(request, 'index.html', {
        'form': form,
        'exchange_date': default_currency.updated_at,
        'output': output
    })
