import pytz
from django.shortcuts import render
from django.utils import timezone

from quantofica.core.forms import NubankExchangeRateForm
from quantofica.core.utils import previous_weekday


def home(request):
    output = None
    date = previous_weekday(timezone.now())
    exchange_date = timezone.datetime(year=date.year, month=date.month, day=date.day,
                                      hour=20, minute=30, second=0, tzinfo=pytz.timezone('America/Sao_Paulo'))
    if 'moeda' in request.GET and 'valor' in request.GET:
        form = NubankExchangeRateForm(request.GET)
        if form.is_valid():
            output = form.calculate()
    else:
        form = NubankExchangeRateForm()
    return render(request, 'index.html', {
        'form': form,
        'exchange_date': exchange_date,
        'output': output
    })
